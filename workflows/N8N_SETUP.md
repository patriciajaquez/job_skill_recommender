# 🔄 N8N Workflow Setup Guide

## 📋 Overview

This guide shows you how to set up and deploy the N8N workflows for automated job market intelligence. The workflows implement the exact architecture from your action plan.

## 🏗️ Architecture

### **Primary Workflow**: `job_market_intelligence_pipeline.json`
```
Schedule (4h) → API Health Check → Decision → API Collection/Backup → Standardization → Validation → Database → Dashboard
```

### **ML Enhancement Workflow**: `ml_enhancement_pipeline.json`
```
Webhook → Skill Extraction (GPT-4) → Salary Prediction (ML) → Trend Analysis → Enriched Dataset → Response
```

## 🚀 Quick Start

### 1. Install N8N

```bash
# Option A: Using Docker (Recommended)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Option B: Using npm
npm install n8n -g
n8n start
```

### 2. Access N8N Interface
- Open browser to `http://localhost:5678`
- Create your N8N account
- You'll see the visual workflow editor

### 3. Import Workflows

**Import Primary Workflow:**
1. In N8N, click "Import from File"
2. Upload `workflows/n8n/job_market_intelligence_pipeline.json`
3. The visual workflow will appear in the editor

**Import ML Enhancement Workflow:**
1. Click "Import from File" again
2. Upload `workflows/n8n/ml_enhancement_pipeline.json`
3. You'll now have both workflows

## ⚙️ Configuration

### Environment Variables

Create `.env` file in your project root:
```bash
# OpenAI for skill extraction
OPENAI_API_KEY=your_openai_api_key_here

# Database connection (when you add database)
AZURE_SQL_CONNECTION=your_database_connection_string

# Slack notifications (optional)
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Job APIs (already configured)
ADZUNA_APP_ID=your_existing_id
ADZUNA_APP_KEY=your_existing_key
# ... (your existing API keys)
```

### N8N Credentials Setup

In N8N interface, go to "Credentials" and add:

1. **HTTP Credentials** for API calls
2. **OpenAI Credentials** for skill extraction
3. **Database Credentials** for data storage
4. **Slack Credentials** for notifications

## 🔧 Workflow Details

### Primary Workflow Nodes

| Node | Purpose | Configuration |
|------|---------|---------------|
| **Schedule Every 4 Hours** | Triggers pipeline | Cron: `0 */4 * * *` |
| **API Health Check** | Tests API availability | Custom function |
| **APIs Healthy?** | Decision logic | If/Then conditions |
| **Parallel API Calls** | Collects job data | Calls Python script |
| **Use Backup Data** | Fallback when APIs down | Mock data generation |
| **Data Standardization** | Cleans and formats data | Data transformation |
| **Quality Validation** | Ensures data quality | Quality checks |
| **Store in Database** | Saves to database | SQL operations |
| **Update Dashboard** | Refreshes metrics | Dashboard API calls |

### ML Enhancement Workflow Nodes

| Node | Purpose | Configuration |
|------|---------|---------------|
| **Webhook Trigger** | Receives job data | POST endpoint |
| **Skill Extraction AI** | GPT-4 skill extraction | OpenAI API calls |
| **Salary Prediction ML** | ML salary predictions | Python ML model |
| **Market Trend Analysis** | Analyzes market trends | Time series analysis |
| **Generate Enriched Dataset** | Creates final dataset | Data combination |
| **Return Results** | Sends response | JSON response |

## 🐍 Python Integration

The workflows use `workflows/scripts/n8n_integration.py` for real API calls:

### Test Python Functions
```bash
# Test job collection
python workflows/scripts/n8n_integration.py collect_jobs "python developer" "remote"

# Test skill extraction
python workflows/scripts/n8n_integration.py extract_skills "Python developer with ML experience"

# Test API health check
python workflows/scripts/n8n_integration.py health_check
```

### Using in N8N
In N8N Function nodes, you can call Python:
```javascript
// Call Python function from N8N
const { execSync } = require('child_process');
const result = execSync('python workflows/scripts/n8n_integration.py collect_jobs "data science" "remote"');
const data = JSON.parse(result.toString());
return data;
```

## 📊 Monitoring and Testing

### Test Primary Workflow
1. In N8N, open the primary workflow
2. Click "Execute Workflow" to test manually
3. Watch data flow through each node
4. Check output at each stage

### Test ML Enhancement
1. Open ML enhancement workflow
2. Send test data to webhook:
```bash
curl -X POST http://localhost:5678/webhook/ml-enhancement \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [
      {
        "id": "test_001",
        "title": "Data Scientist",
        "description": "Python, Machine Learning, SQL required",
        "company": "TechCorp",
        "location": "Remote"
      }
    ]
  }'
```

### Monitor Execution
- N8N provides execution history
- View logs for each node
- Debug failed executions
- Monitor performance metrics

## 🔄 Activation and Scheduling

### Activate Workflows
1. In N8N interface, toggle workflows to "Active"
2. Primary workflow will run every 4 hours automatically
3. ML enhancement waits for webhook triggers

### Manual Triggers
- Click "Execute Workflow" for manual runs
- Use webhook URLs for external triggers
- Test individual nodes during development

## 🌐 Production Deployment

### Docker Compose Setup
```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n
    volumes:
      - ~/.n8n:/home/node/.n8n
      - ./workflows:/home/node/workflows
    depends_on:
      - postgres
      
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Azure Deployment
1. Deploy N8N to Azure Container Instances
2. Use Azure Database for PostgreSQL
3. Configure Azure Key Vault for secrets
4. Set up Application Insights for monitoring

## 🚨 Troubleshooting

### Common Issues

**Workflow not triggering:**
- Check if workflow is active
- Verify cron schedule format
- Check N8N logs

**API calls failing:**
- Verify environment variables
- Test Python integration script
- Check API credentials

**Database connection issues:**
- Verify connection string
- Check database permissions
- Test database connectivity

**Webhook not receiving data:**
- Check webhook URL format
- Verify HTTP method (POST)
- Check Content-Type headers

### Debug Mode
Enable debug logging in N8N:
```bash
export N8N_LOG_LEVEL=debug
n8n start
```

## 📈 Next Steps

1. **Set up database** for persistent storage
2. **Configure Slack notifications** for alerts
3. **Add monitoring dashboards** for metrics
4. **Scale for production** with load balancing
5. **Implement backup strategies** for reliability

## 💡 Tips

- **Start with mock data** to test workflow logic
- **Use N8N's debug mode** to troubleshoot issues
- **Test individual nodes** before full workflow
- **Monitor execution times** for performance
- **Set up alerts** for failed executions

---

**🎉 Your N8N workflows are now ready to automate job market intelligence collection and AI enhancement exactly as planned in your action plan!**
