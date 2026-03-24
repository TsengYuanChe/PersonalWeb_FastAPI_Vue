const API_BASE = import.meta.env.VITE_API_BASE

export async function requestRaw(path) {
  const res = await fetch(`${API_BASE}${path}`)
  const json = await res.json()

  if (!res.ok) {
    throw new Error(json?.error?.message || "Request failed")
  }

  return json
}

export async function request(path) {
  const json = await requestRaw(path)
  return json.data
}
