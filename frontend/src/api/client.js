const API_BASE = import.meta.env.VITE_API_BASE

export async function request(path) {
  const res = await fetch(`${API_BASE}${path}`)
  const json = await res.json()

  if (!res.ok) {
    throw new Error(json?.error?.message || "Request failed")
  }

  return json.data
}

export async function requestWithMeta(path) {
  const res = await fetch(`${API_BASE}${path}`)
  const json = await res.json()

  if (!res.ok) {
    throw new Error(json?.error?.message || "Request failed")
  }

  return {
    data: json.data,
    meta: json.meta,
  }
}
