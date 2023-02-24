<script>
import * as bootstrap from 'bootstrap'
</script>

<template>
  <div id="menu">
    <nav class="navbar bg-light navbar-light navbar-expand-sm">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Radars pédagogiques</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-0">
            <li class="nav-item">
              <router-link class="nav-link active" aria-current="page" to="/">Carte</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/explications">Explications</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>
