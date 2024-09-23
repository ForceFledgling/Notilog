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
function getConfFiles(mode) {
  const modeFiles = [
    '.env',
    mode ? `.env.${mode}` : null,
  ].filter(Boolean);
  
  return modeFiles;
}


/**
 * Проверка существования файла конфигурации в нескольких директориях.
 */
function getConfigFilePath(fileName) {
  // Путь к корню проекта
  const rootPath = path.resolve(process.cwd(), fileName)
  // Путь к директории build/config
  const buildPath = path.resolve('build/config', fileName)

  // Проверяем сначала в корневой директории
  if (fs.existsSync(rootPath)) {
    return rootPath
  }

  // Если не найдено в корне, проверяем в build/config
  if (fs.existsSync(buildPath)) {
    return buildPath
  }

  // Если файл не найден ни в одной из директорий, возвращаем null
  return null
}

/**
 * Загрузка и фильтрация переменных окружения
 */
export function getEnvConfig(match = 'VITE_', mode) {
  const confFiles = getConfFiles(mode);
  let envConfig = {};

  confFiles.forEach((fileName) => {
    const filePath = getConfigFilePath(fileName);

    if (filePath) {
      try {
        const env = dotenv.parse(fs.readFileSync(filePath))
        envConfig = { ...envConfig, ...env }
        console.log(`Загружен файл конфигурации: ${filePath}`)
      } catch (e) {
        console.error(`Ошибка при разборе ${filePath}`, e)
      }
    } else {
      console.warn(`Файл конфигурации ${fileName} не найден в корневой директории и в build/config`)
    }
  });

  const reg = new RegExp(`^(${match})`)
  Object.keys(envConfig).forEach((key) => {
    if (!reg.test(key)) {
      Reflect.deleteProperty(envConfig, key)
    }
  })

  return envConfig
}
