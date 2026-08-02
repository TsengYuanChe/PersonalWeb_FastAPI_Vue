import ezoomLogo from '@/assets/images/exp/ezoom.png'
import nchuLogo from '@/assets/images/exp/nchu.png'
import nycuLogo from '@/assets/images/exp/nycu.png'

const logos = {
  'ezoom.png': ezoomLogo,
  'nchu.png': nchuLogo,
  'nycu.png': nycuLogo,
}

export function getExperienceLogo(filename) {
  return logos[filename] || ''
}
