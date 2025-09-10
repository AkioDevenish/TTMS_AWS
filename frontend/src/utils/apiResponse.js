/**
 * Utility functions to handle API responses in object format
 */

/**
 * Extract data from API response
 * @param {Object} response - Axios response object
 * @returns {*} - The data from the response
 */
export function extractApiData(response) {
  // Handle new object format
  if (response.data && response.data.success && response.data.data !== undefined) {
    return response.data.data;
  }
  
  // Handle old format (direct data)
  return response.data;
}

/**
 * Extract paginated data from API response
 * @param {Object} response - Axios response object
 * @returns {Object} - Object with data and pagination info
 */
export function extractPaginatedData(response) {
  // Handle new object format
  if (response.data && response.data.success && response.data.data !== undefined) {
    return {
      data: response.data.data || [],
      pagination: response.data.pagination || {
        page: 1,
        page_size: 20,
        total_count: 0,
        total_pages: 0,
        has_next: false,
        has_previous: false
      }
    };
  }
  
  // Handle old paginated format
  if (response.data && response.data.results) {
    return {
      data: response.data.results || [],
      pagination: {
        page: response.data.page || 1,
        page_size: response.data.page_size || 20,
        total_count: response.data.count || 0,
        total_pages: response.data.total_pages || 0,
        has_next: response.data.next ? true : false,
        has_previous: response.data.previous ? true : false
      }
    };
  }
  
  // Handle old non-paginated format
  return {
    data: Array.isArray(response.data) ? response.data : [],
    pagination: {
      page: 1,
      page_size: response.data?.length || 0,
      total_count: response.data?.length || 0,
      total_pages: 1,
      has_next: false,
      has_previous: false
    }
  };
}

/**
 * Check if API response indicates success
 * @param {Object} response - Axios response object
 * @returns {boolean} - True if successful
 */
export function isApiSuccess(response) {
  if (response.data && response.data.success !== undefined) {
    return response.data.success === true;
  }
  
  // Assume success for old format if no error
  return response.status >= 200 && response.status < 300;
}

/**
 * Extract error message from API response
 * @param {Object} response - Axios response object
 * @returns {string} - Error message
 */
export function extractApiError(response) {
  if (response.data && response.data.success !== undefined) {
    return response.data.message || 'An error occurred';
  }
  
  // Handle old error format
  if (response.data?.error) {
    return response.data.error;
  }
  
  return 'An error occurred';
}
