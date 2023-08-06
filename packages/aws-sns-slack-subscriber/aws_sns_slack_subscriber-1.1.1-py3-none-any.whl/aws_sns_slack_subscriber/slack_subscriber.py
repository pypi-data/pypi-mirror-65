from aws_cdk import aws_lambda
from aws_cdk.aws_sns import ITopic
from aws_cdk.aws_sns_subscriptions import LambdaSubscription
from aws_cdk.core import Stack
from aws_sns_slack_subscriber import root_path


class SlackSubscriber(aws_lambda.Function):
    def __init__(
            self,
            scope: Stack,
            id: str,
            slack_webhook_url_path: str,
            slack_channel: str,
            sns_topic: ITopic
    ) -> None:
        """
        Constructor.

        :param scope: A Cloud formation stack to which this resource will be added.
        :param id: Resource id.
        :param slack_webhook_url_path: Slack webhook url path. Usually looks like this:
        "/services/T6ZM3ABCS/B011EYRLVPF/Fsrqsc1mgVuX065y9ARNK3QE".
        :param slack_channel: A channel to which send the post. Usually looks like this: "#aws-sns-channel".
        :param sns_topic: A SNS Topic to which this lambda should be subscribed.
        """
        super().__init__(
            scope,
            id,
            code=aws_lambda.Code.from_asset(f'{root_path}/src'),
            handler='lambda.handler',
            runtime=aws_lambda.Runtime.NODEJS_12_X,
            environment={
                'SLACK_WEBHOOK_URL_PATH': slack_webhook_url_path,
                'SLACK_CHANNEL': slack_channel
            }
        )

        sns_topic.add_subscription(LambdaSubscription(self))
