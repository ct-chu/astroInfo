/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
    output: 'export',
    webpack: (config) => { config.externals.push({ sharp: 'commonjs sharp', canvas: 'commonjs canvas' }); return config },
    assetPrefix: process.env.NODE_ENV === "production" ? "http://www.hokoon.edu.hk/astroInfo/" : undefined,
   
    // Optional: Change links `/me` -> `/me/` and emit `/me.html` -> `/me/index.html`
    // trailingSlash: true,
   
    // Optional: Prevent automatic `/me` -> `/me/`, instead preserve `href`
    // skipTrailingSlashRedirect: true,
   
    // Optional: Change the output directory `out` -> `dist`
    // distDir: 'dist',
  }
   
  module.exports = nextConfig

// const isGithubActions = process.env.GITHUB_ACTIONS || false

// let assetPrefix = ''
// let basePath = '/'

// if (isGithubActions) {
//   const repo = process.env.GITHUB_REPOSITORY.replace(/.*?\//, '')

//   assetPrefix = `/${repo}/`
//   basePath = `/${repo}`
// }

// module.exports = {
//   assetPrefix: assetPrefix,
//   basePath: basePath,
// }