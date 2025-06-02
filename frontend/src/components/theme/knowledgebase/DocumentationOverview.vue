<template>
  <div class="col-12 mb-4">
    <div class="card p-4 documentation-overview">
      <h2 class="mb-3">📚 Application Documentation & Overview</h2>
      <p class="lead">Welcome to the MDPS Platform! This page provides a comprehensive overview of how the app works, its architecture, main features, and how to get started as a user or developer.</p>
      <hr />
      <h4>🛠️ Architecture</h4>
      <ul>
        <li><b>Frontend:</b> Vue 3 + Pinia, modern SPA, responsive design, component-based UI.</li>
        <li><b>Backend:</b> Django REST Framework, JWT authentication, modular API endpoints.</li>
        <li><b>Database:</b> MySQL (stations, sensors, users, API keys, logs, etc.)</li>
      </ul>
      <h4>✨ Main Features</h4>
      <ul>
        <li>Weather station and sensor management (add, view, monitor, export data)</li>
        <li>API key management for secure data access</li>
        <li>Real-time and historical data visualization</li>
        <li>Role-based user management (admin, user, support)</li>
        <li>Comprehensive logging and audit trails</li>
        <li>Knowledgebase, support, and documentation modules</li>
      </ul>
      <h4>🔑 Authentication & API Usage</h4>
      <ul>
        <li>All API endpoints require authentication via JWT or API Key.</li>
        <li>API keys can be generated and managed in the API Management section.</li>
        <li>To use an API key, include it in the <code>Authorization: Bearer &lt;API_KEY&gt;</code> header.</li>
        <li>Example: <code>curl -H "Authorization: Bearer &lt;API_KEY&gt;" https://yourdomain/api/measurements/</code></li>
      </ul>
      <h4>👤 User Roles</h4>
      <ul>
        <li><b>Admin:</b> Full access to all features, user and API key management.</li>
        <li><b>User:</b> Access to stations, sensors, and personal API keys.</li>
        <li><b>Support:</b> Can view and assist with user issues, limited management rights.</li>
      </ul>
      <h4>🚀 Quickstart Guide</h4>
      <ol>
        <li>Sign up or log in to your account.</li>
        <li>Navigate to <b>Stations</b> to view and manage weather stations.</li>
        <li>Go to <b>API Management</b> to create and manage your API keys.</li>
        <li>Use the <b>Knowledgebase</b> for help, FAQs, and best practices.</li>
        <li>Check <b>System Logs</b> for audit trails and troubleshooting.</li>
      </ol>
      <h4>📖 More Resources</h4>
      <ul>
        <li>Browse the articles and tutorials below for detailed guides and use cases.</li>
        <li>Contact support via the chat or documentation section for further help.</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
// No script needed for static documentation
</script>

<style scoped>
.documentation-overview {
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.documentation-overview h2 {
  font-weight: 700;
}
.documentation-overview ul, .documentation-overview ol {
  margin-bottom: 1rem;
}
.documentation-overview code {
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.95em;
}
</style> 