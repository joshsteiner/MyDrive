Vue.component('list-entry', {
  props: ['entry'],
  template: `
    <tr>
      <td>{{ entry.type }}</td>
      <td
        v-if="entry.type === 'dir'"
        v-on:click="$root.setDir(entry.id)"
        >
        {{ entry.name }}
      </td>
      <td v-if="entry.type === 'file'">
        {{ entry.name }}
      </td>
      <td></td>
    </tr>
  `,
})

Vue.component('breadcrumbs', {
  props: ['path'],
  template: `
    <div class="breadcrumbs">
      <span
        v-for="d in path"
        v-on:click="$root.setDir(d.id)"
        >
        {{ d.name }}/
      </span>
    </div>
  `,
})

Vue.component('dir-listing', {
  props: ['dir', 'pathToDir'],
  template: `
    <div>
      <div v-if="dir !== null">
        My Drive <breadcrumbs v-bind:path=pathToDir></breadcrumbs>
        <table>
          <tr>
            <th></th>
            <th>name</th>
            <th>size</th>
          </tr>
          <list-entry
            v-for="entry in dir.children"
            v-bind:entry="entry"
            v-bind:key="entry.id"
          />
        </table>
      </div>
      <div v-if="dir === null">
        loading...
      </div>
    </div>
  `,
})

var app = new Vue({
  el: '#app',
  data: {
    rootDir: null,
    dir: null,
    pathToDir: null,
  },
  methods: {
    setRoot: function(newRoot) {
      this.rootDir = newRoot
      this.dir = newRoot
      this.pathToDir = [newRoot]
    },

    setDir: function(newDirID) {
      this.pathToDir = makePath(this.rootDir, newDirID)
      this.dir = this.pathToDir[this.pathToDir.length - 1]
    },
  }
})

function makePath(rootDir, dirID) {
  function searchForPath(path, dirID) {
    const last = path[path.length - 1]
    if (last.id === dirID) {
      return path
    }
    if (last.type !== 'dir' || last.children === []) {
      return null
    }
    return last.children.map(child => {
      return searchForPath(path.concat([child]), dirID)
    }).filter(e => e)[0]
  }
  return searchForPath([rootDir], dirID)
}