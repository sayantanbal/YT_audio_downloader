// API service for YouTube Audio Downloader Backend

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class YouTubeAPIService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    try {
      const response = await fetch(url, { ...defaultOptions, ...options });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async getVideoInfo(url) {
    return this.makeRequest('/video-info', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async startDownload(url) {
    return this.makeRequest('/download', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async getDownloadProgress(downloadId) {
    return this.makeRequest(`/progress/${downloadId}`);
  }

  getDownloadUrl(downloadId) {
    return `${this.baseURL}/download/${downloadId}`;
  }

  async downloadFile(downloadId) {
    const url = this.getDownloadUrl(downloadId);
    
    try {
      const response = await fetch(url);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      // Get filename from Content-Disposition header
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'audio.mp3';
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Create blob and download
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up
      window.URL.revokeObjectURL(downloadUrl);
      
      return { success: true, filename };
    } catch (error) {
      console.error('Download failed:', error);
      throw error;
    }
  }

  async checkHealth() {
    try {
      return await this.makeRequest('/health');
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Utility method to poll download progress
  async pollDownloadProgress(downloadId, onProgress, intervalMs = 1000) {
    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const result = await this.getDownloadProgress(downloadId);
          
          if (result.success) {
            const { progress } = result;
            onProgress(progress);

            if (progress.status === 'completed') {
              resolve(progress);
            } else if (progress.status === 'error') {
              reject(new Error(progress.error || 'Download failed'));
            } else {
              // Continue polling
              setTimeout(poll, intervalMs);
            }
          } else {
            reject(new Error(result.error || 'Failed to get progress'));
          }
        } catch (error) {
          reject(error);
        }
      };

      poll();
    });
  }
}

// Create and export a singleton instance
export const youtubeAPI = new YouTubeAPIService();

// Named exports for individual methods
export const {
  getVideoInfo,
  startDownload,
  getDownloadProgress,
  downloadFile,
  checkHealth,
  pollDownloadProgress
} = youtubeAPI;

export default youtubeAPI;
