// ============================
// SUPABASE CONFIG
// ============================

const SUPABASE_URL = 'https://lanccpfrehhuvmzbzdnr.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxhbmNjcGZyZWhodXZtemJ6ZG5yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY5NTcwMDEsImV4cCI6MjEwMjUzMzAwMX0.fHBynl-sHRl59YmCAXESRseDiXwWHkS0FUi1S0LJvwI';

const supabaseClient = supabase.createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);

// ============================
// STUDY STATE
// ============================

const participantId =
  Date.now().toString(36) +
  Math.random().toString(36).substring(2, 10);
let responses = [];



// ============================
// LOAD CONFIGURATION
// ============================

async function loadStudy() {
  try {
    const response = await fetch("./config.json");

    if (!response.ok) {
      throw new Error(
        `Could not load config.json (${response.status})`
      );
    }

    const config = await response.json();

    if (!Array.isArray(config.subjects)) {
      throw new Error("Invalid config.json");
    }

    buildStudy(config.subjects);

  } catch (error) {
    console.error(error);

    const status = document.getElementById("status");

    if (status) {
      status.textContent =
        "Unable to load the study.";
    }
  }
}


// ============================
// BUILD STUDY
// ============================

function buildStudy(subjects) {

  const container =
    document.getElementById("study-container");

  if (!container) {
    console.error("study-container not found.");
    return;
  }

  container.innerHTML = "";

  subjects.forEach(subject => {

    const methods = [...subject.methods];

    // Randomize the eight methods
    shuffle(methods);

    // ============================
    // SUBJECT BLOCK
    // ============================

    const block =
      document.createElement("section");

    block.className = "subject-block";


    const title =
      document.createElement("h2");

    title.textContent =
      `Subject ${subject.name}`;

    block.appendChild(title);


    // ============================
    // MAIN LAYOUT
    // ============================

    const layout =
      document.createElement("div");

    layout.className =
      "study-layout";


    // ============================
    // INPUT + MASK
    // ============================

    const inputCard =
      document.createElement("div");

    inputCard.className =
      "input-card";

    const inputLabel =
      document.createElement("h3");

    inputLabel.textContent =
      "Input + Mask";

    const inputImage =
      document.createElement("img");

    inputImage.src =
      subject.input_mask;

    inputImage.alt =
      "Input and mask";

    inputCard.appendChild(inputLabel);
    inputCard.appendChild(inputImage);

    layout.appendChild(inputCard);


    // ============================
    // OPTIONS GRID
    // ============================

    const optionsGrid =
      document.createElement("div");

    optionsGrid.className =
      "options-grid";


    methods.forEach((method, index) => {

      const option =
        String.fromCharCode(65 + index);

      const card =
        document.createElement("div");

      card.className =
        "image-card";


      const label =
        document.createElement("h3");

      label.textContent =
        `Option ${option}`;


      const image =
        document.createElement("img");

      image.src =
        method.file;

      image.alt =
        `Option ${option}`;

      image.loading =
        "lazy";


      // ============================
      // CLICK TO SELECT
      // ============================

      card.addEventListener(
        "click",
        () => {

          optionsGrid
            .querySelectorAll(".image-card")
            .forEach(item => {

              item.classList.remove(
                "selected"
              );

            });


          card.classList.add(
            "selected"
          );


          saveResponse(
            subject.name,
            option,
            method.name
          );

        }
      );


      card.appendChild(label);
      card.appendChild(image);

      optionsGrid.appendChild(card);

    });


    layout.appendChild(optionsGrid);

    block.appendChild(layout);

    container.appendChild(block);

  });


  updateProgress();
}


// ============================
// SAVE RESPONSE LOCALLY
// ============================

function saveResponse(
  subjectName,
  option,
  actualMethod
) {

  // Replace previous vote
  // for this subject.
  responses =
    responses.filter(
      response =>
        response.subject_name !==
        subjectName
    );

  responses.push({
    participant_id: participantId,
    subject_name: subjectName,
    selected_option: option,
    actual_method: actualMethod
  });

  updateProgress();
}


// ============================
// PROGRESS
// ============================

function updateProgress() {

  const totalSubjects =
    document.querySelectorAll(
      ".subject-block"
    ).length;

  const completed =
    responses.length;

  const status =
    document.getElementById("status");

  if (status) {

    status.textContent =
      `${completed} / ${totalSubjects} completed`;
  }
}


// ============================
// SHUFFLE
// ============================

function shuffle(array) {

  for (
    let i = array.length - 1;
    i > 0;
    i--
  ) {

    const j =
      Math.floor(
        Math.random() * (i + 1)
      );

    [
      array[i],
      array[j]
    ] = [
        array[j],
        array[i]
      ];
  }
}


// ============================
// SUBMIT
// ============================

async function submitStudy() {

  const submitButton =
    document.getElementById(
      "submit-btn"
    );

  const status =
    document.getElementById(
      "status"
    );

  const totalSubjects =
    document.querySelectorAll(
      ".subject-block"
    ).length;

  // Require all subjects
  if (
    responses.length !==
    totalSubjects
  ) {

    status.textContent =
      `Please select one image for every subject ` +
      `(${responses.length}/${totalSubjects}).`;

    return;
  }

  submitButton.disabled = true;

  status.textContent =
    "Submitting...";

  try {

    const { error } =
      await supabaseClient
        .from("responses")
        .insert(responses);

    if (error) {
      throw error;
    }

    status.textContent =
      "Thank you! Your responses have been submitted.";

    // Prevent duplicate submission
    submitButton.disabled = true;

    document
      .querySelectorAll(".image-card")
      .forEach(card => {
        card.style.pointerEvents = "none";
      });

  } catch (error) {

    console.error(
      "Submission error:",
      error
    );

    status.textContent =
      "Submission failed. Please try again.";

    submitButton.disabled = false;
  }
}


// ============================
// START
// ============================

document.addEventListener(
  "DOMContentLoaded",
  () => {

    loadStudy();

    const submitButton =
      document.getElementById(
        "submit-btn"
      );

    if (submitButton) {

      submitButton.addEventListener(
        "click",
        submitStudy
      );
    }
  }
);