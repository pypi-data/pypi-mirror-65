"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const glob = require("glob");
glob.sync('**/*.ts').forEach((file) => {
    if (file.indexOf('node_modules/') < 0 && file.indexOf('types/') < 0
        && file.indexOf('.test.ts') < 0 && file.indexOf('main.ts')) {
        try {
            Promise.resolve().then(() => require('../../' + file));
        }
        catch (err) {
        }
    }
});
