// next.config.js
const nextConfig = {
    trailingSlash: true,
    output: 'export',
    }


const isGithubActions = process.env.GITHUB_ACTIONS || false

let assetPrefix = ''
let basePath = '/'

if (isGithubActions) {
  const repo = process.env.GITHUB_REPOSITORY.replace(/.*?\//, '')

  assetPrefix = `/${repo}/`
  basePath = `/${repo}`
}

module.exports = nextConfig

module.exports = {
  assetPrefix: assetPrefix,
  basePath: basePath,
}