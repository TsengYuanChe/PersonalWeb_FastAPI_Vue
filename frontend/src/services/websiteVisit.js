const API_URL = 'https://api.adamtseng.com'
const SITE_KEY = 'adamtseng'

export async function trackWebsiteVisit(pagePath) {
  try {
    let visitorId = localStorage.getItem('visitor_id')

    if (!visitorId) {
      visitorId = crypto.randomUUID()
      localStorage.setItem('visitor_id', visitorId)
    }

    const response = await fetch(`${API_URL}/website-visits`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        site_key: SITE_KEY,
        visitor_id: visitorId,
        page_path: pagePath,
      }),
    })

    if (!response.ok) {
      throw new Error(`Website visit tracking failed: ${response.status}`)
    }
  } catch (error) {
    // Tracking errors should not affect normal website navigation
    console.warn('Website visit tracking failed:', error)
  }
}