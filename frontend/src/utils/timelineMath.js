export function monthIndex(date) {
  const match = /^(\d{4})-(\d{2})$/.exec(date ?? '')

  if (!match) {
    return null
  }

  return Number(match[1]) * 12 + Number(match[2]) - 1
}

export function experienceBounds(experience, currentMonthIndex) {
  return {
    start: monthIndex(experience.start_date),
    end: experience.end_date ? monthIndex(experience.end_date) : currentMonthIndex,
  }
}

export function eventFitsExperience(startDate, endDate, experience, currentMonthIndex) {
  const eventStart = monthIndex(startDate)
  const eventEnd = monthIndex(endDate)
  const bounds = experienceBounds(experience, currentMonthIndex)

  return (
    eventStart !== null &&
    eventEnd !== null &&
    bounds.start !== null &&
    bounds.end !== null &&
    eventStart >= bounds.start &&
    eventEnd <= bounds.end
  )
}

export function datePosition(date, experience, currentMonthIndex) {
  const dateValue = monthIndex(date)
  const bounds = experienceBounds(experience, currentMonthIndex)

  if (dateValue === null || bounds.start === null || bounds.end === null) {
    return 0
  }

  const duration = bounds.end - bounds.start

  if (duration <= 0) {
    return 0
  }

  return ((bounds.end - dateValue) / duration) * 100
}
