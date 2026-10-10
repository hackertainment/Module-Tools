import process from "node:process";
import readline from "node:readline";

const rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout,
});

rl.question("What URL should we fetch?\n> ", async (url) => {
	const response = await fetch(url);
	if (!response.ok) {
		if (response.body.toLowerCase().includes("permission")) {  // `response.body` is a stream but not a string and does not have the .toLowerCase() method
			console.error("You didn't have permission to get that URL");
		} else {
			console.error(`The request failed - body: ${response.body}`);
		}
		process.exit(1);
	}

	const contents = await response.json();  // `response` may be an invalid json or not a json format and can throw an exception

	console.log(contents);

	rl.close();
});

// TASK 2
// Read through this file and predict what it does.
// Leave a comment on any lines if you spot any errors, offering an explanation of the problem.
