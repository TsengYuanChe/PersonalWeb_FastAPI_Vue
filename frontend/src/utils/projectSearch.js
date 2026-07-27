const WORD_PATTERN = /[\p{L}\p{N}]+/gu
const SEGMENT_PATTERN = /\S+/gu
const COMPOUND_MARK_PATTERN = /[.+#-]/u
const UNSUPPORTED_COMPOUND_CHARACTERS = /[^\p{L}\p{N}.+#-]+/gu

function normalizeText(value) {
  return String(value ?? '')
    .normalize('NFKC')
    .trim()
    .toLocaleLowerCase()
}

function normalizeCompoundToken(segment) {
  const cleaned = segment
    .replace(UNSUPPORTED_COMPOUND_CHARACTERS, '')
    .replace(/^[-+#]+/u, '')
    .replace(/[.-]+$/u, '')

  if (!cleaned.match(WORD_PATTERN) || !COMPOUND_MARK_PATTERN.test(cleaned)) {
    return ''
  }

  return cleaned
}

export function tokenizeSearchValue(value) {
  const normalized = normalizeText(value)
  const tokens = new Set(normalized.match(WORD_PATTERN) ?? [])

  for (const segment of normalized.match(SEGMENT_PATTERN) ?? []) {
    const compoundToken = normalizeCompoundToken(segment)
    if (compoundToken) {
      tokens.add(compoundToken)
    }
  }

  return [...tokens]
}

function addValues(target, values) {
  for (const value of Array.isArray(values) ? values : []) {
    if (typeof value === 'string' && value.trim()) {
      target.push(value)
    }
  }
}

function addTitledSection(target, section, listKeys) {
  if (!section || typeof section !== 'object') {
    return
  }

  if (section.title) {
    target.push(section.title)
  }

  for (const key of listKeys) {
    addValues(target, section[key])
  }
}

export function collectProjectSearchValues(project) {
  const values = []

  addValues(values, [
    project?.title,
    project?.subtitle,
    project?.category,
    project?.summary,
    project?.role,
    project?.period,
  ])
  addValues(values, project?.technologies)

  addTitledSection(values, project?.overview, ['paragraphs'])
  addTitledSection(values, project?.responsibilities, ['items'])
  addTitledSection(values, project?.architecture, ['paragraphs', 'highlights', 'items'])
  addTitledSection(values, project?.deployment, ['paragraphs', 'highlights', 'items'])
  addTitledSection(values, project?.lessons_learned, ['paragraphs', 'items'])

  if (project?.challenges && typeof project.challenges === 'object') {
    addValues(values, [project.challenges.title])
    for (const challenge of Array.isArray(project.challenges.items)
      ? project.challenges.items
      : []) {
      addValues(values, [challenge?.title, challenge?.description])
    }
  }

  for (const showcaseItem of Array.isArray(project?.showcase) ? project.showcase : []) {
    addValues(values, [
      showcaseItem?.title,
      showcaseItem?.description,
      showcaseItem?.caption,
      showcaseItem?.image_alt,
      showcaseItem?.alt,
    ])
  }

  return values
}

export function tokenizeProjectSearchContent(project) {
  const tokens = new Set()

  for (const value of collectProjectSearchValues(project)) {
    for (const token of tokenizeSearchValue(value)) {
      tokens.add(token)
    }
  }

  return tokens
}

export function matchesProjectSearch(project, query) {
  const queryTokens = tokenizeSearchValue(query)
  if (queryTokens.length === 0) {
    return true
  }

  const projectTokens = tokenizeProjectSearchContent(project)
  return queryTokens.every((token) => projectTokens.has(token))
}

export function uniqueSortedValues(values) {
  const valuesByNormalizedText = new Map()

  for (const value of values) {
    if (typeof value !== 'string' || !value.trim()) {
      continue
    }

    const normalized = normalizeText(value)
    if (!valuesByNormalizedText.has(normalized)) {
      valuesByNormalizedText.set(normalized, value)
    }
  }

  return [...valuesByNormalizedText.values()].sort((left, right) =>
    left.localeCompare(right, undefined, { sensitivity: 'base' }),
  )
}

export function matchesExactValue(value, selectedValue) {
  return normalizeText(value) === normalizeText(selectedValue)
}
