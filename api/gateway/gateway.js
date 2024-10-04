export default function handler(req, res) {
    if (req.method === 'GET') {
        res.status(200).json({ message: "Handled by Node.js" });
    } else {
        res.setHeader('Allow', ['GET']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}