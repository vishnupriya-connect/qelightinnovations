// files.json is generated at publish time from the files in ai_notes/notes/.
export async function loadCatalog() {
  const response = await fetch("files.json");
  if (!response.ok) throw new Error("Lesson list unavailable.");
  const paths = await response.json();
  if (!Array.isArray(paths)) throw new Error("Invalid lesson list.");

  const lessons = {};
  for (const path of paths) {
    if (typeof path !== "string") continue;
    const match = path.match(/^notes\/(QAI\.\d+(?:\.\d+)+)_([^/]+)_Notes\.md$/);
    if (!match) continue;
    const [, id, slug] = match;
    if (Object.hasOwn(lessons, id)) throw new Error("Duplicate lesson ID: " + id);
    lessons[id] = {
      title: slug.replaceAll("_", " "),
      note: path,
      resources: []
    };
  }

  for (const path of paths) {
    if (typeof path !== "string") continue;
    const match = path.match(/^notes\/(QAI\.\d+(?:\.\d+)+)_resources\/(.+)$/);
    if (!match || !Object.hasOwn(lessons, match[1])) continue;
    lessons[match[1]].resources.push({label: match[2].replaceAll("/", " / "), url: path});
  }

  const compareIDs = (left, right) => {
    const a = left.slice(4).split(".").map(Number), b = right.slice(4).split(".").map(Number);
    for (let i = 0; i < Math.max(a.length, b.length); i++) {
      if (a[i] !== b[i]) return (a[i] ?? -1) - (b[i] ?? -1);
    }
    return 0;
  };
  return Object.fromEntries(Object.keys(lessons).sort(compareIDs).map(id => {
    lessons[id].resources.sort((a, b) => a.url.localeCompare(b.url));
    return [id, lessons[id]];
  }));
}
