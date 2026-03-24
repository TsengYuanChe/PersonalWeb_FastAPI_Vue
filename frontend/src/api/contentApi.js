import { requestRaw } from "./client"

export async function getAbout() {
  const res = await requestRaw("/api/v1/about")
  return {
    content: res.data,
    updatedAt: res.meta?.updated_at ?? null,
  }
}

export async function getExperience() {
  const res = await requestRaw("/api/v1/experience")
  return {
    content: res.data,
    updatedAt: res.meta?.updated_at ?? null,
  }
}

export async function getProjects() {
  const res = await requestRaw("/api/v1/projects")
  return {
    content: res.data,
    updatedAt: res.meta?.updated_at ?? null,
  }
}
