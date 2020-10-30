# Software Analysis

## Project goal

Polp Fiction is an in-house tool developed by [Mercadolibre](https://www.mercadolibre.com.ar/) that aims expose metrics of the current situation regarding privileges  based on identities and access  on the cloud.  

### Phase 0

Its main objective is to show a clear vision on how the business is in terms of Users, Roles and API privileges in the cloud, centralize all this data in a single query point where specific data can be obtained to make strategic decisions that can Phase improve the access management security between all our different identities in the cloud.  

### Phase 1

---

## Tools analyzed

These were some of the already existing tools evaluated.

* [Policy Sentry](https://github.com/salesforce/policy_sentry)

  * AWS IAM Least Privilege Policy Generator, auditor, and analysis database. It compiles database tables based on the AWS IAM Documentation on [Actions, Resources, and Condition Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html) and leverages that data to create least-privilege IAM policies.

* [Cloudsplaning](https://github.com/salesforce/cloudsplaining)

  * Cloudsplaining identifies violations of least privilege in AWS IAM policies and generates a pretty HTML report with a triage worksheet. It can scan all the policies in your AWS account or it can scan a single policy file.

* [Repokid](https://github.com/Netflix/repokid) + [Aardvark](https://github.com/Netflix-Skunkworks/aardvark)

  * Repokid uses Access Advisor provided by [Aardvark](https://github.com/Netflix-Skunkworks/aardvark) to remove permissions granting access to unused services from the inline policies of IAM roles in an AWS account.

* [Security Monkey](https://github.com/Netflix/security_monkey)

  * Security Monkey monitors your [AWS and GCP accounts](https://medium.com/@Netflix_Techblog/netflix-security-monkey-on-google-cloud-platform-gcp-f221604c0cc7) for policy changes and alerts on insecure configurations. Support is available for OpenStack public and private clouds. Security Monkey can also watch and monitor your GitHub organizations, teams, and repositories. It provides a single UI to browse and search through all of your accounts, regions, and cloud services. The monkey remembers previous states and can show you exactly what changed, and when.

* [Policy Universe](https://github.com/Netflix-Skunkworks/policyuniverse)

  * Policy Universe is a python package that provides classes to parse AWS IAM and Resource Policies.
  
  

| Tool                                                         | Goal fulfillment | Exceeds the Goal | Metrics | Support |
| ------------------------------------------------------------ | ---------------- | --------------- | ---- | ------------------------------------------------------------ |
| [Policy Sentry](https://github.com/salesforce/policy_sentry) | 0%               | NO              | NO |  |
| [Cloudsplaning](https://github.com/salesforce/cloudsplaining) | 90%              | YES             | "YES" |  |
| [Security Monkey](https://github.com/Netflix/security_monkey) | 100%             | YES             | YES |  |
| [Policy Universe](https://github.com/Netflix-Skunkworks/policyuniverse) | 0%               | NO              | NO |  |
| [Repokid](https://github.com/Netflix/repokid)                | 30%              | NO              | NO |  |
| [Aardvark](https://github.com/Netflix-Skunkworks/aardvark)   | 0%               | NO              | NO (has the data) |  |
| [Cloudux](https://github.com/Netflix-Skunkworks/cloudaux) | 0 | NO | NO |  |



