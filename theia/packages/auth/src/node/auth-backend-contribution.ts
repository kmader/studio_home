/*
 * Deep Learning Studio - GUI platform for designing Deep Learning AI without programming
 *
 * Copyright (C) 2016-2018 Deep Cognition Inc.
 *
 * All rights reserved.
 */

import { injectable, inject } from 'inversify';
import * as http from 'http';
import * as https from 'https';
import * as express from 'express';
import { ILogger } from "@theia/core/lib/common";
import { BackendApplicationContribution } from '@theia/core/lib/node';

let fs = require('fs');

@injectable()
export class AuthBackendContribution implements BackendApplicationContribution {
    constructor(
        @inject(ILogger) protected readonly logger: ILogger) {
    }

    configure(app: express.Application) {

        app.use ("/", function (req, res, next) {
            if (req.path === "/") {
                if ("session" in req.query) {
                    let filename = '/home/theia/.token';
                    if (process.env.DLS_ROOT) {
                        filename = process.env.DLS_ROOT + filename;
                    }
                    let contents = fs.readFileSync(filename, 'utf8');
                    if (contents === req.query["session"]) {
                        next();
                    } else {
                        res.sendStatus(404);
                    }
                } else {
                    console.log("no session found");
                }
            } else {
                next();
            }
          });
    }

    onStart(server: http.Server | https.Server): void {

    }
}
