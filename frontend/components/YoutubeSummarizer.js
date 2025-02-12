const YouTubeSummarizer = {
  template: `
    <div class="card p-4">
      <h3>AI Powered YouTube Video Summarizer</h3>
      <p>Enter a YouTube link to add it to your list.</p>

      <div class="input-group mb-3">
        <input v-model="newLink" type="text" class="form-control" placeholder="Enter YouTube link" />
        <button @click="addLink" class="btn btn-primary">Add</button>
      </div>

      <div class="row">
        <div class="col-md-6">
          <button @click="summarizeLinks" class="btn btn-success mt-3 w-100">Summarize</button>
        </div>
      </div>

      <div class="card mt-3">
        <div class="card-body">
          <h5 class="card-title">Your Uploaded Links</h5>
          <ul class="list-group">
            <li v-for="link in links" :key="link.id" class="list-group-item d-flex justify-content-between align-items-center">
              <span><a :href="link.url">{{ link.url }}</a></span>
              <button @click="deleteLink(link.id)" class="btn btn-danger btn-sm">Delete</button>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="summary" class="card mt-3">
        <div class="card-body">
          <h5 class="card-title">Summary</h5>
          <p>{{ summary }}</p>
        </div>
      </div>

      <!-- Talk to the Database Section -->
      <div class="card mt-3">
        <div class="card-body">
          <h5 class="card-title">Talk to the Database</h5>
          <div class="input-group mb-3">
            <input v-model="query" type="text" class="form-control" placeholder="Enter your query" />
            <button @click="askDatabase" class="btn btn-info">Ask</button>
          </div>
          <div v-if="dbResponse">
            <h6>Response:</h6>
            <p>{{ dbResponse }}</p>
          </div>
        </div>
      </div>
    </div>
  `,

  data() {
    return {
      newLink: "",
      links: [],
      summary: "",
      query: "",
      dbResponse: "",
    };
  },

  methods: {
    async addLink() {
      if (!this.newLink.trim()) return alert("Please enter a valid link.");

      const res = await fetch("/api/youtube_links", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authentication-Token": this.$store.state.authen_token },
        body: JSON.stringify({ url: this.newLink }),
      });

      if (res.ok) {
        const data = await res.json();
        this.links.push({ id: data.id, url: this.newLink });
        this.newLink = "";
      } else {
        alert("Failed to add link.");
      }
    },

    async deleteLink(linkId) {
      const res = await fetch(`/api/youtube_links/${linkId}`, {
        method: "DELETE",
        headers: { "Authentication-Token": this.$store.state.authen_token }
      });

      if (res.ok) {
        this.links = this.links.filter(link => link.id !== linkId);
      } else {
        alert("Failed to delete link.");
      }
    },

    async summarizeLinks() {
      const res = await fetch("/api/summarize", { 
      method: "GET",
      headers: { "Authentication-Token": this.$store.state.authen_token }
       });

      if (res.ok) {
        const data = await res.json();
        this.summary = data.summary;
      } else {
        alert("Failed to get summary.");
      }
    },

    async askDatabase() {
      if (!this.query.trim()) return alert("Please enter a query.");

      const res = await fetch("/api/query_database", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authentication-Token": this.$store.state.authen_token },
        body: JSON.stringify({ query: this.query }),
      });

      if (res.ok) {
        const data = await res.json();
        this.dbResponse = data.response;
      } else {
        alert("Failed to query the database.");
      }
    },
  },

  async mounted() {
    const res = await fetch("/api/youtube_links", {
      headers: { "Authentication-Token": this.$store.state.authen_token },
  });

    if (res.ok) {
      this.links = await res.json();
    }
  },
};

export default YouTubeSummarizer;
