---
layout: page
permalink: /publications/
title: Publications
description: Selected Publications.
nav: true
nav_order: 4
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

{% if site.plugins contains 'jekyll-scholar' %}

<div class="publications">
{% bibliography %}
</div>
{% else %}
<p>Publications listing requires <code>jekyll-scholar</code>. The site will include it during the GitHub Actions build.</p>p
{% endif %}
