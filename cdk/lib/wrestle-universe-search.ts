/** @format */

import {
  Stack,
  StackProps,
  Duration,
  RemovalPolicy,
  aws_lambda as lambda,
  aws_iam as iam,
  aws_events as events,
  aws_events_targets as targets,
  aws_s3 as s3,
} from "aws-cdk-lib";
import { Construct } from "constructs";

// CONFIG
const RUNTIME = lambda.Runtime.PYTHON_3_11;
const APP_DIR_PATH = "../src";
const LAYER_ZIP_PATH = "../dependencies.zip";

export class WrestleUniverseSearch extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // S3バケットを作成
    const bucket = new s3.Bucket(this, "WrestlerUniverseSearchBucket", {
      bucketName: "wrestler-universe-search-koboriakira",
      removalPolicy: RemovalPolicy.DESTROY,
    });

    const role = this.makeRole(bucket.bucketArn);
    const myLayer = this.makeLayer();

    // Lambda: graphql API
    const graphql = this.createLambdaFunction(
      "Graphql",
      role,
      myLayer,
      "graphql_app.handler",
      30,
      true
    );

    // Lambda: pull_episode
    const pullEpisode = this.createLambdaFunction(
      "PullEpisode",
      role,
      myLayer,
      "pull_episode.handler",
      900,
      false
    );
  }

  /**
   * Create or retrieve an IAM role for the Lambda function.
   * @returns {iam.Role} The created or retrieved IAM role.
   */
  makeRole(bucketArn: string) {
    // Lambda の実行ロールを作成
    const role = new iam.Role(this, "LambdaRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    // 管理ポリシーを追加
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );

    // ユーザポリシーを追加
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["lambda:InvokeFunction", "lambda:InvokeAsync"],
        resources: ["*"],
      })
    );
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["s3:*"],
        resources: [bucketArn + "/*"],
      })
    );

    return role;
  }

  /**
   * Create or retrieve a Lambda layer.
   * @returns {lambda.LayerVersion} The created or retrieved Lambda layer.
   */
  makeLayer() {
    return new lambda.LayerVersion(this, "Layer", {
      code: lambda.Code.fromAsset(LAYER_ZIP_PATH), // レイヤーの内容を含むディレクトリ
      compatibleRuntimes: [RUNTIME], // このレイヤーが互換性を持つランタイム
    });
  }

  /**
   * Create a Lambda function.
   * @param {iam.Role} role The IAM role for the Lambda function.
   * @param {lambda.LayerVersion} myLayer The Lambda layer to be used.
   * @returns {lambda.Function} The created Lambda function.
   */
  createLambdaFunction(
    name: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    handler: string,
    timeout: number = 30,
    function_url_enabled: boolean = false
  ): lambda.Function {
    const fn = new lambda.Function(this, name, {
      runtime: RUNTIME,
      handler: handler,
      code: lambda.Code.fromAsset(APP_DIR_PATH),
      role: role,
      layers: [myLayer],
      timeout: Duration.seconds(timeout),
    });

    fn.addEnvironment("DUMMY", process.env.DUMMY || "");

    if (function_url_enabled) {
      fn.addFunctionUrl({
        authType: lambda.FunctionUrlAuthType.NONE, // 認証なし
      });
    }

    return fn;
  }
}
