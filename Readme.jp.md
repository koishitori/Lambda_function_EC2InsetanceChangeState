# EC2制御Lambda関数

このAWS Lambda関数は、タグに基づいてEC2インスタンスの起動や停止を行うことができます。EventBridgeを使用した夜間の定期停止や、AWS Change Calendarを利用した不定期な停止など、様々なシナリオで活用できる汎用的なEC2インスタンス管理ツールです。

## 関数の概要

この関数は以下の構造のJSONペイロードを受け取ります：

```json
{
  "region": string,  # 対象リージョン
  "tagName": string, # 対象EC2インスタンスのタグ名
  "action": string,  # start（起動）またはstop（停止）
  "test": bool       # テストモード（true/false）
}
```

### 機能

1. 指定された`tagName`の値が`action`または"true"であるEC2インスタンスIDを取得します。
2. `action`が"start"の場合、インスタンスIDとNameタグを表示し、インスタンスを起動します（`test`がtrueの場合を除く）。
3. `action`が"stop"の場合、インスタンスIDとNameタグを表示し、インスタンスを停止します（`test`がtrueの場合を除く）。

## セットアップ

1. AWSアカウントで新しいLambda関数を作成します。
2. ランタイムとしてPython 3.12を使用します。
3. 提供されたPythonコードをLambda関数にコピーします。
4. 適切なIAMロールを設定し、必要最小限の権限を付与します（IAMポリシーセクションを参照）。

## IAMポリシー

Lambda関数の実行ロールに以下のIAMポリシーを付与してください：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

このポリシーは、EC2インスタンスの詳細取得、起動/停止、およびログの書き込みに必要な権限を付与します。

## 使用方法

Lambda関数をJSONペイロードで呼び出します。例：

```json
{
  "region": "ap-northeast-1",
  "tagName": "Environment",
  "action": "start",
  "test": false
}
```

これにより、ap-northeast-1リージョンで"Environment"タグの値が"start"または"true"であるすべてのEC2インスタンスが起動されます。

## テスト

ペイロードの`test`パラメータを`true`に設定すると、実際にインスタンスを起動/停止せずに関数を実行できます。これにより、どのインスタンスが影響を受けるかを確認できます。

## ログ

関数は、インスタンスIDとそのNameタグ、および実行されたアクションをCloudWatch Logsに記録します。詳細な実行情報については、Lambda関数のCloudWatchロググループを確認してください。
