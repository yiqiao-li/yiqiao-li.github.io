---
layout: page
title: Research
permalink: /projects/
nav: true
nav_order: 1
display_categories: [Current, Past]
horizontal: true
---

<div class="research-intro">
  <p class="research-intro-text">
    Our research focuses on advancing transportation systems through artificial intelligence, advanced sensing technologies, and data-driven methods. We develop solutions for traffic monitoring, vehicle classification, vulnerable road user safety, urban freight analytics, and policy evaluation.
  </p>

  <div class="research-pillars">
    <span class="pillar"><i class="fas fa-brain"></i> AI & Sensing</span>
    <span class="pillar"><i class="fas fa-user-shield"></i> VRU Safety</span>
    <span class="pillar"><i class="fas fa-truck"></i> Urban Freight</span>
    <span class="pillar"><i class="fas fa-chart-line"></i> Policy & Simulation</span>
    <span class="pillar"><i class="fas fa-database"></i> Data Analytics</span>
  </div>

  {% assign current_count = site.projects | where: "category", "Current" | size %}
  {% assign past_count = site.projects | where: "category", "Past" | size %}
  <div class="research-stats">
    <a href="#Current" class="stat-badge">
      <strong>{{ current_count }}</strong> Active
    </a>
    <a href="#Past" class="stat-badge">
      <strong>{{ past_count }}</strong> Completed
    </a>
  </div>
</div>

<div class="projects projects-showcase">
{% if site.enable_project_categories and page.display_categories %}
  {% for category in page.display_categories %}
  <div id="{{ category }}" class="category-section">
    <h2 class="category">{{ category }}</h2>
    {% assign categorized_projects = site.projects | where: "category", category %}
    {% assign sorted_projects = categorized_projects | sort: "year" | reverse %}
    <div class="row">
    {% for project in sorted_projects %}
      {% include projects_showcase.liquid %}
    {% endfor %}
    </div>
  </div>
  {% endfor %}
{% else %}
  {% assign sorted_projects = site.projects | sort: "year" | reverse %}
  <div class="row">
  {% for project in sorted_projects %}
    {% include projects_showcase.liquid %}
  {% endfor %}
  </div>
{% endif %}
</div>
