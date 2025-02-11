import Navbar from "../components/Navbar.js";
import YouTubeSummarizer from "../components/YoutubeSummarizer.js";
import PDFSummarizer from "../components/PDFSummarizer.js";
import ImageSummarizer from "../components/ImageSummarizer.js";

const MainDashboard = {
  template: `
    <div>
      <Navbar></Navbar>
      <div class="container mt-4">
        <div class="d-flex justify-content-center">
          <button @click="changeSection('youtube')" class="btn btn-outline-primary me-4" :class="{ active: section == 'youtube' }">YouTube Videos</button>
          <button @click="changeSection('pdf')" class="btn btn-outline-success me-4" :class="{ active: section == 'pdf' }">PDF Files</button>
          <button @click="changeSection('image')" class="btn btn-outline-warning" :class="{ active: section == 'image' }">Images</button>
        </div>

        <div class="card mt-4">
          <div class="card-body">
            <div v-if="section == 'youtube'">
              <h2><u>YouTube Videos</u></h2>
              <p>Summarize YouTube videos using their links.</p>
              <YouTubeSummarizer></YouTubeSummarizer>
            </div>

            <div v-if="section == 'pdf'">
              <h2><u>PDF Files</u></h2>
              <p>Summarize PDF files.</p>
              <PDFSummarizer></PDFSummarizer>
            </div>

            <div v-if="section == 'image'">
              <h2><u>Images</u></h2>
              <p>Summarize content in images.</p>
              <ImageSummarizer></ImageSummarizer>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,

  data() {
    return {
      section: 'youtube', // Default section
    };
  },

  methods: {
    changeSection(mode) {
      this.section = mode;
    },
  },

  components: {
    Navbar,
    YouTubeSummarizer,
    PDFSummarizer,
    ImageSummarizer,
  },
};

export default MainDashboard;
