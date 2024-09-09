import fs from 'fs'
import path from 'path'
import dotenv from 'dotenv'

/**
 * * Корневой путь проекта
 * @descrition Путь не содержит завершающего слэша (/)
 */
export function getRootPath() {
  return path.resolve(process.cwd())
}

/**
 * * Путь к директории src проекта
 * @param srcName Название директории src (по умолчанию: "src")
 * @descrition Путь не содержит завершающего слэша (/)
 */
export function getSrcPath(srcName = 'src') {
  return path.resolve(getRootPath(), srcName)
}

export function convertEnv(envOptions) {
  const result = {}
  if (!envOptions) return result

  for (const envKey in envOptions) {
    let envVal = envOptions[envKey]
    if (['true', 'false'].includes(envVal)) envVal = envVal === 'true'

    if (['VITE_PORT'].includes(envKey)) envVal = +envVal

    result[envKey] = envVal
  }
  return result
}

/**
 * Получение имен файлов конфигурации, действительных в текущей среде
 */
function getConfFiles() {
  const script = process.env.npm_lifecycle_script
  const reg = new RegExp('--mode ([a-z_\\d]+)')
  const result = reg.exec(script)
  if (result) {
    const mode = result[1]
    return ['.env', '.env.local', `.env.${mode}`]
  }
  return ['.env', '.env.local', '.env.production']
}

export function getEnvConfig(match = 'VITE_', confFiles = getConfFiles()) {
  let envConfig = {}
  confFiles.forEach((item) => {
    try {
      if (fs.existsSync(path.resolve(process.cwd(), item))) {
        const env = dotenv.parse(fs.readFileSync(path.resolve(process.cwd(), item)))
        envConfig = { ...envConfig, ...env }
      }
    } catch (e) {
      console.error(`Ошибка при разборе ${item}`, e)
    }
  })
  const reg = new RegExp(`^(${match})`)
  Object.keys(envConfig).forEach((key) => {
    if (!reg.test(key)) {
      Reflect.deleteProperty(envConfig, key)
    }
  })
  return envConfig
}
