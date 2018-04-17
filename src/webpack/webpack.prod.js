const webpack = require("webpack");
const merge = require('webpack-merge');
const parts = require('./webpack.parts');
const common = require('./webpack.common');
const path = require('path');

module.exports = merge([
  common,
  {
    performance: {
      hints: "warning",
      maxEntrypointSize: 100000,
      maxAssetSize: 450000,
    },
    output: {
      filename: "js/[name].bundle.js",
    },
    recordsPath: path.join(__dirname, "records.json"),
  },
  parts.clean(['static'], parts.PATHS.assets),
  parts.extractBundles([{
      name: "vendor",
      minChunks: ({
        resource
      }) => /node_modules/.test(resource),
    },
    {
      name: "manifest",
      minChunks: Infinity,
    },
  ]),
  parts.minifyJavaScript({}),
  parts.minifyCSS({
    options: {
      discardComments: {
        removeAll: true,
        safe: true,
      },
    },
  }),

  parts.loadImages({
    options: {
      limit: 15000,
      name: "[name].[ext]",
    },
  }),
  parts.setFreeVariable("process.env.NODE_ENV", "production"),
]);
