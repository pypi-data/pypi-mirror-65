var https = require('https');
var util = require('util');

exports.handler = function(event, context) {
    var message = event.Records[0].Sns.Message;
    var subject = event.Records[0].Sns.Subject;
    var eventSource = event.Records[0].EventSource;

    console.log(JSON.stringify(event, null, 2));

    var dangerMessages = [
        " but with errors",
        " to RED",
        "During an aborted deployment",
        "Failed to deploy application",
        "Failed to deploy configuration",
        "has a dependent object",
        "is not authorized to perform",
        "Pending to Degraded",
        "Stack deletion failed",
        "Unsuccessful command execution",
        "You do not have permission",
        "Your quota allows for 0 more running instance"
    ];

    var warningMessages = [
        " aborted operation.",
        " to YELLOW",
        "Adding instance ",
        "Degraded to Info",
        "Deleting SNS topic",
        "is currently running under desired capacity",
        "Ok to Info",
        "Ok to Warning",
        "Pending Initialization",
        "Removed instance ",
        "Rollback of environment"
    ];

    var severity = "good";

    for (let item of dangerMessages) {
        if (message.includes(item)) {
            severity = "danger";
            break;
        }
    }

    if (severity === "good") {
        for (let item of warningMessages) {
            if (message.includes(item)) {
                severity = "warning";
                break;
            }
        }
    }

    var postData = {
        "channel": process.env.SLACK_CHANNEL,
        "username": eventSource,
        "text": "*" + subject + "*",
        "icon_emoji": ":arrow_forward:",
        "attachments": [{
            "color": severity,
            "text": message
        }]
    };

    var options = {
        method: 'POST',
        hostname: 'hooks.slack.com',
        port: 443,
        path: process.env.SLACK_WEBHOOK_URL_PATH
    };

    var req = https.request(options, function(res) {
        res.setEncoding('utf8');
        res.on('data', function(chunk) {
            context.done(null);
        });
    });

    req.on('error', function(e) {
        console.log('Problem with request: ' + e.message);
    });

    req.write(util.format("%j", postData));
    req.end();
};
