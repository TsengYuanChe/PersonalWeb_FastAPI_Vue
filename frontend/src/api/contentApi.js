import { request, requestWithMeta } from "./client"

export const getAbout = () => request("/api/v1/about")
export const getExperience = () => request("/api/v1/experience")
export const getProjects = () => request("/api/v1/projects")

export const getAboutWithMeta = () => requestWithMeta("/api/v1/about")
export const getExperienceWithMeta = () => requestWithMeta("/api/v1/experience")
export const getProjectsWithMeta = () => requestWithMeta("/api/v1/projects")
