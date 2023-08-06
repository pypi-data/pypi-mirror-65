## AWS SNS Slack Subscriber

A library that creates a slack subscriber to your aws sns topic.

#### Remarks

The project is written by [Laimonas Sutkus](https://github.com/laimonassutkus) and is owned by 
[iDenfy](https://github.com/idenfy). This is an open source
library intended to be used by anyone. [iDenfy](https://github.com/idenfy) aims
to share its knowledge and educate market for better and more secure IT infrastructure.

#### Related technology

This project utilizes the following technology:

- *AWS* (Amazon Web Services).
- *AWS CDK* (Amazon Web Services Cloud Development Kit).
- *AWS Lambda*.
- *AWS Sns*.
- *Slack*.

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```bash
pip install aws_sns_slack_subscriber
```

Or directly install it through source.

```bash
./build.sh -ic
```

### Description

When you have SNS Topics, you may subscribe to them with various ways. For example, 
email subscription will send an email to a desired email address when a notification 
is pushed to a SNS Topic. Most of the time email subscription is not ideal as it may 
clutter your email box. Hence, there are other ways to subscribe to a SNS Topic. We 
think the most convenient way to subscribe to SNS Topic is a Lambda Function integration
which sends callbacks to your specified Slack channel. This library project is about that.
It creates a "Slack subscription" with a help of Lambda.

### Examples

Create sns slack subscriber as any other lambda function:

```python
from aws_sns_slack_subscriber.slack_subscriber import SlackSubscriber

lambda_function_slack_subscirber = SlackSubscriber(...)
```
