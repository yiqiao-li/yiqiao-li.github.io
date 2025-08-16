# Docker Setup and Website Preview Guide

## Overview

This guide explains how to run the AI & Mobility Research Lab website locally using Docker and preview it at `http://localhost:8080`.

## Prerequisites

- Docker Desktop installed and running
- Git repository cloned locally
- Terminal/Command Prompt access

## Quick Start

### 1. Navigate to Project Directory

```bash
cd yiqiao-li.github.io
```

### 2. Start Docker Container

```bash
docker-compose up -d
```

### 3. Access Website

Open your web browser and navigate to:

```
http://localhost:8080
```

## Detailed Instructions

### Docker Configuration

The project includes pre-configured Docker files:

- **Dockerfile**: Defines the Jekyll environment
- **docker-compose.yml**: Orchestrates the container setup

**Key Configuration:**

- **Image**: `amirpourmand/al-folio:v0.13.4` (pre-built Jekyll image)
- **Port Mapping**: `8080:8080` (local:container)
- **LiveReload**: `35729:35729` for automatic browser refresh
- **Volume Mounting**: Local files mounted to `/srv/jekyll`
- **Environment**: Development mode enabled

### Container Management

#### Check Status

```bash
docker-compose ps
```

#### View Logs

```bash
docker-compose logs jekyll
```

#### Stop Container

```bash
docker-compose down
```

#### Restart Container

```bash
docker-compose restart
```

#### Rebuild Container (if needed)

```bash
docker-compose up --build
```

## Website Features

### Available Pages

- **Home**: Lab overview and PI profile
- **Research**: Current and past projects
- **Publications**: Academic papers and citations
- **People**: Team members and profiles
- **Teaching**: Course information
- **Service**: Professional activities

### Technical Features

- ✅ **Responsive Design**: Works on desktop, tablet, mobile
- ✅ **Light/Dark Mode**: Toggle between themes
- ✅ **Live Reload**: Automatic browser refresh on file changes
- ✅ **MathJax Support**: Mathematical notation rendering
- ✅ **BibTeX Integration**: Publication management
- ✅ **GitHub Integration**: Repository statistics
- ✅ **Search Functionality**: Site-wide content search

## Troubleshooting

### Common Issues

#### Port Already in Use

**Problem**: `Error: Port 8080 is already in use`
**Solution**:

1. Change port in `docker-compose.yml`:
   ```yaml
   ports:
     - 8081:8080 # Use port 8081 instead
   ```
2. Access website at `http://localhost:8081`

#### Container Won't Start

**Problem**: Container fails to start
**Solutions**:

1. Ensure Docker Desktop is running
2. Check available disk space
3. Restart Docker Desktop
4. Run `docker system prune` to clean up

#### Website Not Loading

**Problem**: Browser shows connection error
**Solutions**:

1. Wait 30-60 seconds for Jekyll build to complete
2. Check container logs: `docker-compose logs jekyll`
3. Verify container is running: `docker-compose ps`

#### File Changes Not Reflecting

**Problem**: Updates not showing in browser
**Solutions**:

1. Ensure LiveReload is working (port 35729)
2. Hard refresh browser (Ctrl+F5)
3. Check file permissions
4. Restart container: `docker-compose restart`

### Performance Optimization

#### Build Time

- Initial build: ~30-60 seconds
- Subsequent builds: ~5-15 seconds
- File changes: Near-instant with LiveReload

#### Resource Usage

- **Memory**: ~500MB-1GB
- **CPU**: Low usage during idle
- **Disk**: ~2-5GB for container and dependencies

## Development Workflow

### Making Changes

1. Edit files in your local directory
2. Changes automatically detected by Jekyll
3. Browser refreshes automatically (LiveReload)
4. No manual restart required for most changes

### File Types Supported

- **Markdown**: `.md` files for content
- **Liquid Templates**: `.liquid` files for layouts
- **SCSS/CSS**: Styling files
- **JavaScript**: Interactive features
- **Images**: JPG, PNG, GIF, WebP formats

### Recommended Tools

- **Code Editor**: VS Code, Sublime Text, or similar
- **Browser**: Chrome, Firefox, Safari, Edge
- **Terminal**: Command Prompt, PowerShell, or Git Bash

## Alternative Access Methods

If `localhost` doesn't work, try:

- `http://127.0.0.1:8080`
- `http://0.0.0.0:8080`
- Your machine's IP address: `http://[YOUR_IP]:8080`

## Security Notes

- Container runs in development mode
- No production security measures enabled
- Intended for local development only
- Don't expose to public networks

## Cleanup

### Stop and Remove Container

```bash
docker-compose down
```

### Remove All Related Data

```bash
docker-compose down -v
docker system prune -f
```

## Support

For issues related to:

- **Docker**: Check Docker Desktop documentation
- **Jekyll**: Refer to Jekyll documentation
- **al-folio Theme**: Check the [al-folio repository](https://github.com/alshedivat/al-folio)
- **Website Content**: Contact the lab PI, Dr. Yiqiao Li

---

**Last Updated**: August 2024  
**Version**: 1.0  
**Maintained By**: AI & Mobility Research Lab
