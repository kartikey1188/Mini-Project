const PDFSummarizer = {
  template: `
    <div class="card p-4">
      <h3>AI Powered PDF Summarizer</h3>
      <p>Upload a PDF file to add it to your list.</p>

      <div class="input-group mb-3">
        <input type="file" accept=".pdf" @change="handleFileUpload" class="form-control">
        <button @click="uploadFile" class="btn btn-primary" :disabled="!selectedFile">Upload</button>
      </div>

      <div class="row">
        <div class="col-md-6">
          <button @click="summarizeFiles" class="btn btn-success mt-3 w-100">Summarize</button>
        </div>
      </div>

      <div class="card mt-3">
        <div class="card-body">
          <h5 class="card-title">Your Uploaded PDFs</h5>
          <ul class="list-group">
            <li v-for="file in pdfFiles" :key="file.id" class="list-group-item d-flex justify-content-between align-items-center">
              <span><span @click="openFile(file.file_path)" class="text-primary" style="cursor: pointer;">{{ file.file_name }}</span></span>
              <button @click="deleteFile(file.id)" class="btn btn-danger btn-sm">Delete</button>
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
      selectedFile: null,
      pdfFiles: [],
      summary: "",
      query: "",
      dbResponse: "",
    };
  },

  methods: {
    openFile(filePath) {
      window.open(filePath, "_blank");
    },
    
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },

    async uploadFile() {
      if (!this.selectedFile) return alert("Please select a file.");

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      const res = await fetch("/api/pdf_files", {
        method: "POST",
        body: formData,
        headers: { "Authentication-Token": this.$store.state.authen_token }
      });

      if (res.ok) {
        this.selectedFile = null;
        this.fetchFiles();
      } else {
        alert("Failed to upload file.");
      }
    },

    async fetchFiles() {
      const res = await fetch("/api/pdf_files", {
        headers: { "Authentication-Token": this.$store.state.authen_token },
      });
      if (res.ok) {
        this.pdfFiles = await res.json();
      }
    },

    async deleteFile(fileId) {
      const res = await fetch(`/api/pdf_files/${fileId}`, {
        method: "DELETE",
        headers: { "Authentication-Token": this.$store.state.authen_token }
      });

      if (res.ok) {
        this.pdfFiles = this.pdfFiles.filter(file => file.id !== fileId);
      } else {
        alert("Failed to delete file.");
      }
    },

    async summarizeFiles() {
      const res = await fetch("/api/pdf_summarize", { 
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
    this.fetchFiles();
  },
};

export default PDFSummarizer;
