import ezoomLogo from '@/assets/images/journey/ezoom.png'
import nchuLogo from '@/assets/images/journey/nchu.png'
import nycuLogo from '@/assets/images/journey/nycu.png'

const logos = {
  'ezoom.png': ezoomLogo,
  'nchu.png': nchuLogo,
  'nycu.png': nycuLogo,
}

export function getJourneyLogo(filename) {
  return logos[filename] || ''
}
