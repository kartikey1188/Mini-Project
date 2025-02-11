const YouTubeSummarizer = {
    template: `
      <div class="card p-4">
        <h3>YouTube Video Summarizer</h3>
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
                <span>{{ link.url }}</span>
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
      </div>
    `,
  
    data() {
      return {
        newLink: "",
        links: [],
        summary: "",
      };
    },
  
    methods: {
      async addLink() {
        if (!this.newLink.trim()) return alert("Please enter a valid link.");
  
        const res = await fetch("/api/youtube_links", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
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
        });
  
        if (res.ok) {
          this.links = this.links.filter(link => link.id !== linkId);
        } else {
          alert("Failed to delete link.");
        }
      },
  
      async summarizeLinks() {
        const res = await fetch("/api/summarize", { method: "GET" });
  
        if (res.ok) {
          const data = await res.json();
          this.summary = data.summary;
        } else {
          alert("Failed to get summary.");
        }
      },
    },
  
    async mounted() {
      const res = await fetch("/api/youtube_links");
  
      if (res.ok) {
        this.links = await res.json();
      }
    },
  };
  
  export default YouTubeSummarizer;  