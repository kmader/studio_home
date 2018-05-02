/*
 * Copyright (C) 2017 Ericsson and others.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 */

import { injectable, inject, named } from 'inversify';
import * as os from 'os';
import { ILogger } from '@theia/core/lib/common/logger';
import { TerminalProcess, TerminalProcessOptions, ProcessManager, MultiRingBuffer } from '@theia/process/lib/node';
import { isWindows } from "@theia/core/lib/common";
import URI from "@theia/core/lib/common/uri";
import { FileUri } from "@theia/core/lib/node/file-uri";
import { parseArgs } from '@theia/process/lib/node/utils';

export const ShellProcessFactory = Symbol("ShellProcessFactory");
export type ShellProcessFactory = (options: ShellProcessOptions) => ShellProcess;

export const ShellProcessOptions = Symbol("ShellProcessOptions");
export interface ShellProcessOptions {
    shell?: string,
    rootURI?: string,
    cols?: number,
    rows?: number,
    userId?: string,
    environment?: string
}

let path = require("path");

function getRootPath(rootURI?: string): string {
    if (rootURI) {
        const uri = new URI(rootURI);
        return FileUri.fsPath(uri);
    } else {
        return os.homedir();
    }
}

@injectable()
export class ShellProcess extends TerminalProcess {

    protected static defaultCols = 80;
    protected static defaultRows = 24;

    constructor(
        @inject(ShellProcessOptions) options: ShellProcessOptions,
        @inject(ProcessManager) processManager: ProcessManager,
        @inject(MultiRingBuffer) ringBuffer: MultiRingBuffer,
        @inject(ILogger) @named("terminal") logger: ILogger
    ) {
        process.env["USERID"] = options.userId;
        process.env["HOME"] = "/data/" + options.userId;
        process.env["ENVIRONMENT"] = options.environment;

        super(<TerminalProcessOptions>{
            command: options.shell || ShellProcess.getShellExecutablePath(),
            args: ShellProcess.getShellExecutableArgs(),
            options: {
                name: 'xterm-color',
                cols: options.cols || ShellProcess.defaultCols,
                rows: options.rows || ShellProcess.defaultRows,
                cwd: getRootPath(options.rootURI),
                env: process.env as any
            }
        }, processManager, ringBuffer, logger);
    }

    protected static getShellExecutablePath(): string {
        const shell = process.env.THEIA_SHELL;
        if (shell) {
            return shell;
        }
        if (isWindows) {
            return path.join(process.env.DLS_ROOT_WIN, "usr", "bin", "bash.exe");
        } else {
            return process.env.SHELL!;
        }
    }

    protected static getShellExecutableArgs(): string[] {
        const args = process.env.THEIA_SHELL_ARGS;
        if (args) {
            return parseArgs(args);
        }
        return [];
    }
}
