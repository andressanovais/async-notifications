resource "aws_iam_role" "scheduler_role" {
  name = "notification-scheduler-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "scheduler.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "scheduler_policy" {
  name   = "notification-scheduler-policy"
  policy = file("./iam_policies/policy_notification_scheduler.json")
}

resource "aws_iam_role_policy_attachment" "scheduler_role_policy" {
  role       = aws_iam_role.scheduler_role.name
  policy_arn = aws_iam_policy.scheduler_policy.arn
}


resource "aws_iam_role" "lambda_base_role" {
  name               = "lambda-base-role"
  assume_role_policy = file("./iam_policies/lambda_assume_role.json")
}

resource "aws_iam_policy" "lambda_base_policy" {
  name   = "lambda-base-policy"
  policy = file("./iam_policies/policy_lambda_base.json")
}
