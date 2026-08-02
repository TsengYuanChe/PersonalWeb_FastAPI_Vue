export function monthIndex(date) {
  const match = /^(\d{4})-(\d{2})$/.exec(date ?? '')

  if (!match) {
    return null
  }

  return Number(match[1]) * 12 + Number(match[2]) - 1
}

export function journeyBounds(journeyItem, currentMonthIndex) {
  return {
    start: monthIndex(journeyItem.start_date),
    end: journeyItem.end_date ? monthIndex(journeyItem.end_date) : currentMonthIndex,
  }
}

export function eventFitsJourney(startDate, endDate, journeyItem, currentMonthIndex) {
  const eventStart = monthIndex(startDate)
  const eventEnd = monthIndex(endDate)
  const bounds = journeyBounds(journeyItem, currentMonthIndex)

  return (
    eventStart !== null &&
    eventEnd !== null &&
    bounds.start !== null &&
    bounds.end !== null &&
    eventStart >= bounds.start &&
    eventEnd <= bounds.end
  )
}

export function datePosition(date, journeyItem, currentMonthIndex) {
  const dateValue = monthIndex(date)
  const bounds = journeyBounds(journeyItem, currentMonthIndex)

  if (dateValue === null || bounds.start === null || bounds.end === null) {
    return 0
  }

  const duration = bounds.end - bounds.start

  if (duration <= 0) {
    return 0
  }

  return ((bounds.end - dateValue) / duration) * 100
}
