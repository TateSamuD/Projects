const path = require('path');

module.exports = {
  entry: './src/ffmpeg.js', // Entry point for your FFmpeg code
  output: {
    filename: 'ffmpeg.bundle.js', // The bundled file
    path: path.resolve(__dirname, 'dist'), // Output directory
  },
  mode: 'production', // Use 'development' for debugging
  resolve: {
    fallback: {
      fs: false, // Ignore Node.js-specific modules (like fs)
      path: require.resolve('path-browserify'), // Use path-browserify for browser
    },
  },
};
