#!/usr/bin/env node
/** @format */

import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { WrestleUniverseSearch } from "../lib/wrestle-universe-search";

const app = new cdk.App();
new WrestleUniverseSearch(app, "WrestleUniverseSearch", {});
