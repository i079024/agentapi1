// Enhanced execution and AI report functions
function executeAllTests() {
    if (!confirm('Execute all tests? This may take some time.')) return;
    
    showExecutionProgress('Executing all tests...');
    
    fetch(`${API_BASE}/execute-all-tests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(result => {
        hideExecutionProgress();
        if (result.status === 'success') {
            const s = result.summary;
            alert(`✅ Execution Complete!\nTotal: ${s.total_tests}, Passed: ${s.passed}, Failed: ${s.failed}\nSuccess Rate: ${s.success_rate}%`);
            sessionStorage.setItem('last_execution_results', JSON.stringify(result));
        } else {
            throw new Error(result.detail || 'Execution failed');
        }
    })
    .catch(error => {
        hideExecutionProgress();
        alert(`Execution failed: ${error.message}`);
    });
}

function executeCollection(collectionName) {
    if (!confirm(`Execute collection "${collectionName}"?`)) return;
    
    showExecutionProgress(`Executing collection: ${collectionName}...`);
    
    fetch(`${API_BASE}/execute-collection/${encodeURIComponent(collectionName)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(result => {
        hideExecutionProgress();
        if (result.status === 'success') {
            const s = result.summary;
            alert(`✅ Collection Complete!\nTotal: ${s.total_tests}, Passed: ${s.passed}, Failed: ${s.failed}`);
            sessionStorage.setItem('last_execution_results', JSON.stringify(result));
        } else {
            throw new Error(result.detail || 'Collection execution failed');
        }
    })
    .catch(error => {
        hideExecutionProgress();
        alert(`Collection execution failed: ${error.message}`);
    });
}

function generateAIReport() {
    const lastResults = sessionStorage.getItem('last_execution_results');
    if (!lastResults) {
        alert('No execution results. Please execute tests first.');
        return;
    }
    
    const executionData = JSON.parse(lastResults);
    
    showExecutionProgress('Generating AI report...');
    
    fetch(`${API_BASE}/generate-ai-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            execution_results: executionData.results,
            collection_name: executionData.collection || 'API Tests'
        })
    })
    .then(response => response.json())
    .then(result => {
        hideExecutionProgress();
        if (result.status === 'success') {
            const report = result.report;
            alert(`🤖 AI Report Generated!\n\nFile: ${report.filename}\nFormat: ${report.format || 'Word'}\nSaved to: ${report.filepath}\n\nIncludes:\n• Test summary\n• AI suggestions\n• Performance insights\n• Security recommendations`);
        } else {
            throw new Error(result.detail || 'Report generation failed');
        }
    })
    .catch(error => {
        hideExecutionProgress();
        alert(`Report failed: ${error.message}\n\nNote: Install python-docx for Word format`);
    });
}

function showExecutionProgress(message) {
    const div = document.createElement('div');
    div.id = 'execution-progress';
    div.style.cssText = `
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        background: white; border: 2px solid #007bff; border-radius: 8px; padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); z-index: 10000; text-align: center; min-width: 300px;
    `;
    div.innerHTML = `
        <div style="margin-bottom: 15px; font-weight: bold;">${message}</div>
        <div style="width: 100%; height: 4px; background: #eee; border-radius: 2px;">
            <div style="width: 100%; height: 100%; background: #007bff; animation: pulse 1.5s infinite;"></div>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: #666;">Please wait...</div>
    `;
    document.body.appendChild(div);
}

function hideExecutionProgress() {
    const div = document.getElementById('execution-progress');
    if (div) div.remove();
}