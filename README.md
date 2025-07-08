# CV Site

A clean, professional CV/resume website built with modern web standards. Features responsive design, PDF export functionality, and seamless integration with the daza.ar ecosystem.

> **📁 Part of the daza.ar Ecosystem**: This repository is part of the [daza.ar-env](https://github.com/juanmanueldaza/daza.ar-env) development environment. For local development setup, unified workflow, and cross-site documentation, see the [main repository](https://github.com/juanmanueldaza/daza.ar-env).

## 🌐 Live Site

Visit the live CV at: **[cv.daza.ar](https://cv.daza.ar)**

## ✨ Features

- 📱 **Fully Responsive** - Adapts perfectly to mobile, tablet, and desktop
- 📄 **PDF Export** - Download CV as PDF with one click
- 🎨 **Modern Design** - Clean, professional styling
- ♿ **Accessible** - ARIA labels and keyboard navigation
- 🚀 **Fast Loading** - Optimized performance and minimal dependencies
- 📝 **Markdown Content** - Content served from remote markdown files
- 🧭 **Integrated Navigation** - Uses the daza.ar navbar component
- 🔄 **Live Updates** - Content updates automatically from data repository

## 🏗️ Architecture

This CV site uses a **remote module architecture**:

- **Content**: Imported from [data.daza.ar](https://data.daza.ar/md/) markdown files
- **Navigation**: Uses [navbar.daza.ar](https://navbar.daza.ar) component
- **Markdown Processing**: Uses [mdsite.daza.ar](https://mdsite.daza.ar/mdsite.js) module
- **PDF Generation**: Integrated PDF export functionality

## 🚀 Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom properties
- **Vanilla JavaScript** - ES6 modules for functionality
- **Remote Modules** - Shared components from daza.ar ecosystem
- **GitHub Pages** - Static site hosting with custom domain

## 📁 File Structure

```
cv/
├── CNAME          # Custom domain configuration
├── index.html     # Main HTML file
└── README.md      # This file
```

## 🛠️ Development

### Local Development

Use the [daza.ar-env](https://github.com/juanmanueldaza/daza.ar-env) development environment:

```bash
# Clone the development environment
git clone https://github.com/juanmanueldaza/daza.ar-env.git
cd daza.ar-env

# Setup all sites (including this one)
./setup.sh

# Start development servers
./dev.sh

# CV site will be available at:
# http://cv.local:3001
```

### Content Updates

Content is managed in the [data repository](https://github.com/juanmanueldaza/data):

1. Edit markdown files in the data repository
2. Changes automatically reflect on the live site
3. No need to redeploy this repository

### Deployment

Deployment is handled automatically via GitHub Pages:

```bash
# Manual deployment (if needed)
npm run deploy
```

## 🎨 Customization

### Styling

The site uses CSS custom properties for easy theming:

```css
:root {
  --window-bg: #1a1a1a;
  --window-border: #333;
  --link: #4a9eff;
  --link-hover: #66b3ff;
}
```

### Content Structure

Content is loaded from remote markdown with these sections:

- **Header**: Name, title, contact information
- **Summary**: Professional summary
- **Experience**: Work history
- **Education**: Academic background
- **Skills**: Technical and soft skills
- **Projects**: Notable projects and achievements

## 🔧 Configuration

The site automatically configures:

- **Navbar**: Contact links and PDF export button
- **Content**: Remote markdown loading from data.daza.ar
- **PDF**: Filename and export settings
- **Accessibility**: ARIA labels and keyboard navigation

## 🏗️ Ecosystem Integration

This CV site is part of the **daza.ar ecosystem**:

- **🛠️ Development Environment**: [daza.ar-env](https://github.com/juanmanueldaza/daza.ar-env) - Unified development setup
- **📋 Contributing**: Follow the branch workflow in [daza.ar-env/CONTRIBUTING.md](https://github.com/juanmanueldaza/daza.ar-env/blob/main/CONTRIBUTING.md)
- **🎯 Issues & Features**: Use the [feature_improvement.md](https://github.com/juanmanueldaza/daza.ar-env/blob/main/.github/ISSUE_TEMPLATE/feature_improvement.md) template
- **🏗️ Architecture**: See [deployment documentation](https://github.com/juanmanueldaza/daza.ar-env/blob/main/docs/DEPLOYMENT.md)

### Related Sites

- **📋 Onepager**: [onepager.daza.ar](https://onepager.daza.ar) - One-page portfolio version
- **🏠 Start Page**: [start.daza.ar](https://start.daza.ar) - Personal dashboard
- **🧭 Navbar**: [navbar.daza.ar](https://navbar.daza.ar) - Navigation component
- **📝 Mdsite**: [mdsite.daza.ar](https://mdsite.daza.ar) - Markdown processing utilities
- **📊 Data**: [data.daza.ar](https://data.daza.ar) - Content repository
- **🖼️ Wallpapers**: [wallpapers.daza.ar](https://wallpapers.daza.ar) - Wallpaper collection

## 📱 Browser Support

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

Contributions welcome! Please use the unified development environment:

1. Use [daza.ar-env](https://github.com/juanmanueldaza/daza.ar-env) for development setup
2. Follow the [contributing guidelines](https://github.com/juanmanueldaza/daza.ar-env/blob/main/CONTRIBUTING.md)
3. Use the [feature template](https://github.com/juanmanueldaza/daza.ar-env/blob/main/.github/ISSUE_TEMPLATE/feature_improvement.md) for new features

### Content Contributions

- **CV Content**: Edit markdown files in [data repository](https://github.com/juanmanueldaza/data)
- **Site Functionality**: Contribute to this repository or shared modules
- **Design**: Update CSS or suggest UX improvements

## 👤 Author

**Juan Manuel Daza**

- Website: [daza.ar](https://daza.ar)
- GitHub: [@juanmanueldaza](https://github.com/juanmanueldaza)
- LinkedIn: [juanmanueldaza](https://www.linkedin.com/in/juanmanueldaza)
- Email: juanmanueldaza@gmail.com

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Made with ❤️ as part of the <a href="https://github.com/juanmanueldaza/daza.ar-env">daza.ar ecosystem</a></p>
  <p>
    <a href="https://cv.daza.ar">Live Site</a> •
    <a href="https://github.com/juanmanueldaza/daza.ar-env">Development Environment</a> •
    <a href="https://github.com/juanmanueldaza/daza.ar-env/issues">Report Issue</a>
  </p>
</div>