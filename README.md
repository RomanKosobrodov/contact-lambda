# contact-lambda

URL Lambda for sending contact forms from static websites

## What it does

If you host a static website on AWS you can use this lambda function to send contact information forms to your chosen email. This lambda function uses [AWS Simple Email Service](https://ap-southeast-2.console.aws.amazon.com/ses/home?region=ap-southeast-2#/homepage), which is much cheaper compared to contact form services available from other providers.

This repository contains the source code and a Serverless Application Model (SAM) template for deploying this lambda function.

## Prerequisites

Obviously, you need an AWS account with sufficient permissions to create resources in CloudFormation. You also need to [verify your email](https://docs.aws.amazon.com/ses/latest/dg/verify-addresses-and-domains.html) to send emails from SES.

## Deployment

You can launch the template by following [this link](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=contact-lambda&templateURL=https://templates-kosobrodov-net.s3.amazonaws.com/contact-lambda/template.yaml).

Alternatively, clone the repository, install [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) if you don't have it already, check that you have sufficient permissions to create the template, and run the following commands:

```bash
sam build
sam deploy --guided
```

Wait till the deployment is complete and save the `Lambda Function URL Endpoint` which should look like this:
`https://13apwmrj3uhrdpmo4chw7fpcnq0vmqef.lambda-url.ap-southeast-2.on.aws/`

## Input parameters

The following input parameters must be defined in the template:

| Parameter      | Description                                                                  | Example                 |
| -------------- | ---------------------------------------------------------------------------- | ----------------------- |
| HostURL        | The URL of your website. This parameter is mandatory.                        | https://github.com      |
| RedirectPage   | The page to which the user is redirected after submitting the form.          | thankyou.html           |
| ErrorPage      | This page is displayed when an error is occurred while sending the form.     | error.html              |
| SenderEmail    | Email address verified in AWS SES to appear in the _From_ field on the email | no-reply-aws@amazon.com |
| RecipientEmail | The email address to which the contact form message is sent.                 | info@example.com        |
| CCEmail        | (Optional) When specified a "carbon copy" is sent to this email.             | support@example.com     |
| BCCEmail       | (Optional) When specified a "blind carbon copy" is also sent.                | marketing@example.com   |

## Usage

To send an email from your contact page, create a form and post it to the endpoint. The following inputs are required: `sender`, `email` and `message`. When the function successfully completes it redirects to the "Thank you" page. If an error occurs the user is redirected to the error page. For security reasons no information on the actual cause of the error is transmitted to the client. To troubleshoot the problem inspect the CloudWatch logs.

An example of the contact form is included in this repository. Please update the `action` parameter of the form with the `Lambda Function URL Endpoint`. Using the example above, this would look like:

```html
<form
  class="contact-form"
  action="https://13apwmrj3uhrdpmo4chw7fpcnq0vmqef.lambda-url.ap-southeast-2.on.aws/"
  method="post"
></form>
```

This is the only configurable parameter that needs to be modified before you are ready to use the form.

## Issues and feedback

If you find this repository useful please give it a star. Use GitHub Issues to report problems with the code.
