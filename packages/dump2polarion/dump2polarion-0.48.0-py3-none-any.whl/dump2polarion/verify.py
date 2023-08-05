"""Verifies that data were updated in Polarion."""

import logging
import os
import time

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


_DEFAULT_TIMEOUT = 600
_DEFAULT_DELAY = 10

_NOT_FINISHED_STATUSES = ("ready", "running")


class QueueSearch:
    """Search for jobs in the completed jobs queue."""

    def __init__(self, session, queue_url, log_url):
        self.session = session
        self.queue_url = queue_url
        self.log_url = log_url
        self.skip = False

    def download_queue(self, job_ids):
        """Download data of completed jobs."""
        if self.skip:
            return None

        url = "{}?jobtype=completed&jobIds={}".format(
            self.queue_url, ",".join(str(x) for x in job_ids)
        )
        try:
            response = self.session.get(url, headers={"Accept": "application/json"})
            if response:
                response = response.json()
            else:
                response = None
        # pylint: disable=broad-except
        except Exception as err:
            logger.error(err)
            response = None

        return response

    def find_jobs(self, job_ids):
        """Find the jobs in the completed job queue."""
        matched_jobs = []
        if self.skip:
            return matched_jobs

        json_data = self.download_queue(job_ids)
        if not json_data:
            return matched_jobs

        jobs = json_data["jobs"]
        for job in jobs:
            if (
                job.get("id") in job_ids
                and job.get("status", "").lower() not in _NOT_FINISHED_STATUSES
            ):
                matched_jobs.append(job)

        return matched_jobs

    def wait_for_jobs(self, job_ids, timeout, delay):
        """Wait until the jobs appears in the completed job queue."""
        found_jobs = []

        if self.skip:
            return found_jobs

        logger.debug("Waiting up to %d sec for completion of the job IDs %s", timeout, job_ids)

        remaining_job_ids = set(job_ids)

        countdown = timeout
        while countdown > 0:
            matched_jobs = self.find_jobs(remaining_job_ids)
            if matched_jobs:
                remaining_job_ids.difference_update({job["id"] for job in matched_jobs})
                found_jobs.extend(matched_jobs)
            if not remaining_job_ids:
                return found_jobs
            time.sleep(delay)
            countdown -= delay

        logger.error(
            "Timed out while waiting for completion of the job IDs %s. Results not updated (yet).",
            list(remaining_job_ids),
        )

    def _check_outcome(self, jobs):
        """Parse returned messages and check submit outcome."""
        if self.skip:
            return False

        if not jobs:
            logger.error("Import failed!")
            return False

        failed_jobs = []
        for job in jobs:
            status = job.get("status")
            if not status:
                failed_jobs.append(job)
                continue

            if status.lower() != "success":
                failed_jobs.append(job)

        for job in failed_jobs:
            logger.error("job: %s; status: %s", job.get("id"), job.get("status"))
        if len(failed_jobs) == len(jobs):
            logger.error("Import failed!")
        elif failed_jobs:
            logger.error("Some import jobs failed!")
        else:
            logger.info("Results successfully updated!")

        return not failed_jobs

    def _download_log(self, url, output_file):
        """Save log returned by the message bus."""
        logger.info("Saving log %s to %s", url, output_file)

        def _do_log_download():
            try:
                return self.session.get(url)
            # pylint: disable=broad-except
            except Exception as err:
                logger.error(err)

        # log file may not be ready yet, wait a bit
        for __ in range(5):
            log_data = _do_log_download()
            if log_data or log_data is None:
                break
            time.sleep(2)

        if not (log_data and log_data.content):
            logger.error("Failed to download log file %s.", url)
            return
        with open(os.path.expanduser(output_file), "ab") as out:
            out.write(log_data.content)

    def get_logs(self, jobs, log_file=None):
        """Get log or log url of the jobs."""
        if not (jobs and self.log_url):
            return

        for job in jobs:
            url = "{}?jobId={}".format(self.log_url, job.get("id"))
            if log_file:
                self._download_log("{}&download".format(url), log_file)
            else:
                logger.info("Submit log for job %s: %s", job.get("id"), url)

    def verify_submit(self, job_ids, timeout, delay, **kwargs):
        """Verify that the results were successfully submitted."""
        if self.skip:
            return False

        jobs = self.wait_for_jobs(job_ids, timeout, delay)
        self.get_logs(jobs, log_file=kwargs.get("log_file"))

        return self._check_outcome(jobs)


def get_queue_obj(session, queue_url, log_url):
    """Check that all the data that is needed for submit verification is available."""
    skip = False
    if not queue_url:
        logger.error("The queue url is not configured, skipping submit verification")
        skip = True

    if not session:
        logger.error("Missing requests session, skipping submit verification")
        skip = True
    queue = QueueSearch(session=session, queue_url=queue_url, log_url=log_url)
    queue.skip = skip
    return queue


# pylint: disable=too-many-arguments
def verify_submit(
    session, queue_url, log_url, job_ids, timeout=_DEFAULT_TIMEOUT, delay=_DEFAULT_DELAY, **kwargs
):
    """Verify that the results were successfully submitted."""
    verification_queue = get_queue_obj(session=session, queue_url=queue_url, log_url=log_url)
    return verification_queue.verify_submit(job_ids, timeout, delay, **kwargs)
