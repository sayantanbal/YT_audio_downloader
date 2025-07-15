# 🚀 AWS Elastic Beanstalk Deployment Guide

## Prerequisites
- AWS Account with appropriate permissions
- AWS CLI configured
- EB CLI installed: `pip install awsebcli`

## 📋 Deployment Steps

### 1. Build Frontend
```bash
cd YT_audio_downloader
npm run build
mkdir -p build
cp -r dist/* build/
```

### 2. Initialize Elastic Beanstalk
```bash
# Initialize EB application
eb init

# Follow the prompts:
# - Region: Choose your preferred region (e.g., us-east-1)
# - Application name: youtube-audio-downloader
# - Platform: Python 3.11
# - CodeCommit: No (unless you want to use it)
```

### 3. Create Environment
```bash
# Create production environment
eb create production

# This will:
# - Create EC2 instance
# - Set up load balancer
# - Configure auto-scaling
# - Deploy your application
```

### 4. Deploy Updates
```bash
# For future deployments
eb deploy production
```

### 5. Monitor Application
```bash
# View logs
eb logs

# Check health
eb health

# Open in browser
eb open
```

## 🔧 Configuration Options

### Environment Variables
Set these in EB Console or via CLI:
```bash
eb setenv FLASK_ENV=production
eb setenv SECRET_KEY=your-secret-key-here
eb setenv CORS_ORIGINS=https://your-domain.com
```

### Custom Domain
```bash
# Add custom domain in EB Console
# Configure SSL certificate
# Update CORS_ORIGINS accordingly
```

## 💰 Cost Optimization

### Single Instance (Low Traffic)
- Remove load balancer
- Use t3.micro instance
- Cost: ~$10/month

```bash
# Configure single instance
eb config

# In editor, set:
# Environment Type: SingleInstance
# Instance Type: t3.micro
```

### Auto-Scaling (High Traffic)
- Keep load balancer
- Use t3.small+ instances
- Set min/max instances
- Cost: ~$25-50/month

## 🔍 Troubleshooting

### Common Issues:
1. **FFmpeg not found**: Check .ebextensions/01_packages.config
2. **Import errors**: Verify application.py path configuration
3. **Permission denied**: Check temp directory permissions
4. **CORS errors**: Update CORS_ORIGINS environment variable

### Debug Commands:
```bash
# SSH into instance
eb ssh

# Check logs
eb logs --all

# View environment info
eb status
```

## 🌐 Frontend Options

### Option 1: Serve from Same EB App
- Frontend files in `/build` directory
- Served as static files via Flask
- Single domain, no CORS issues

### Option 2: Separate Frontend (S3 + CloudFront)
- Deploy React build to S3
- Use CloudFront for CDN
- Update CORS settings in backend
- Better performance for global users

## 🔐 Security Considerations

### Production Settings:
- Set `FLASK_ENV=production`
- Use strong `SECRET_KEY`
- Enable HTTPS
- Set up proper CORS origins
- Implement rate limiting
- Add request size limits

### Monitoring:
- Enable AWS CloudWatch
- Set up health check alarms
- Monitor costs
- Track usage patterns

## 📈 Scaling

### Vertical Scaling:
- Upgrade instance type (t3.micro → t3.small → t3.medium)

### Horizontal Scaling:
- Enable auto-scaling
- Set min/max instances based on CPU/memory usage

### Caching:
- Add ElastiCache for Redis
- Implement download caching
- Use CloudFront for static assets

## 🚀 Go Live Checklist

- [ ] Build and test locally
- [ ] Configure production environment variables
- [ ] Deploy to EB
- [ ] Test all functionality
- [ ] Set up custom domain (optional)
- [ ] Configure SSL certificate
- [ ] Set up monitoring and alerts
- [ ] Update README with live URL
- [ ] Add terms of service and privacy policy
