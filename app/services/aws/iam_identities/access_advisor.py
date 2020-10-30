from cloudaux.aws.decorators import rate_limited
import time


class AccessAdvisor():

    def __init__(self, iam):
        self.client = iam
        self.max_access_advisor_job_wait = 5 * 60  # Wait 5 minutes before giving up on jobs

    def get_last_access_data(self, arns):
        jobs = self._generate_job_ids(arns)
        details = self._get_job_results(jobs)
        if arns and not details:
            print("Didn't get any results from Access Advisor")
        return details

    @rate_limited()
    def _generate_service_last_accessed_details(self, arn):
        try:
            return self.client.generate_service_last_accessed_details(Arn=arn)['JobId']
        except Exception as e:
            print(e)
            return None

    @rate_limited()
    def _get_service_last_accessed_details(self, job_id):
        try:
            return self.client.get_service_last_accessed_details(JobId=job_id)
        except Exception as e:
            print(e)
            return None

    def _generate_job_ids(self, arns):
        jobs = {}
        for arn in arns:
            job_id = self._generate_service_last_accessed_details(arn)
            if not job_id:
                print(f"Could not get jobs for entity: {arn}")
                continue
            jobs[job_id] = arn
        return jobs

    def _get_job_results(self, jobs):
        access_details = {}
        # jobs = {"d876198276s918276s987s6a98f76" : "arn:iam:us-east-1:12312312321312:policy/Altapoliciy", ...}
        job_queue = list(jobs.keys())
        # last_job_completion_time = time.time()
        while job_queue:
            # Pull next job ID
            job_id = job_queue.pop()
            details = self._get_service_last_accessed_details(job_id)
            if not details:
                print('Could not gather data from {0}.'.format(jobs[job_id]))
                continue
            # Check for job failure
            if details['JobStatus'] != 'COMPLETED':
                if details['JobStatus'] == 'IN_PROGRESS':
                    if len(job_queue) == 1:
                        print("Wainting for 1989.. we don't want no more war")
                        time.sleep(5)
                    job_queue.insert(0,job_id)
                print(f"Job {job_id} status: {details['JobStatus']} for ARN {jobs[job_id]}.")
                continue

            access_details[jobs[job_id]] = {each.pop('ServiceNamespace'): each for each in details["ServicesLastAccessed"]}

        return access_details

