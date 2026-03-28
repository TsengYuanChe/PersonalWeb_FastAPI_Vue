export function useProjectHelpers() {
    function safeArray(value) {
    return Array.isArray(value) ? value : []
    }

    function isFeaturedProject(project) {
        return project?.type === 'featured'
    }

    function previewEngineering(project) {
        return safeArray(project?.engineering).slice(0, 2)
    }

    function getGithubLink(project) {
        return project?.links?.github || ''
    }

    function getDemoLink(project) {
        return project?.links?.demo || ''
    }

    return {
        safeArray,
        isFeaturedProject,
        previewEngineering,
        getGithubLink,
        getDemoLink
    }
}