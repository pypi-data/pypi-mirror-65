const path = require('path');

var webpack = require('webpack');


module.exports = {
    externals: {
        jquery: 'jQuery'
    },
    entry: './NearBeach/build/index.js',
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ['to-string-loader', 'css-loader'],
            },
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({$: 'jquery', jQuery: 'jquery' }),
    ],
    output: {
        publicPath: "/js/",
        path: path.join(__dirname, '/NearBeach/static/NearBeach/js/'),
        filename: 'NearBeach.bundle.js'
    },
};