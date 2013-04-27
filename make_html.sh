if [ $# -ne 1 ]
then 
	echo "Wrong number of arguments!"
fi
python parse.py $1 | pandoc -s -c stylesheet/A4resume.css --from=markdown --to=html5 | sed "s/<\/h1>/<\/h1><div>/" | sed "s/<h2/<\/div><h2/" | sed "s/<\/h2>/<\/h2><div class=\"content\">/" | sed "s/<\/body>/<\/div><\/body>/" > resume.html
