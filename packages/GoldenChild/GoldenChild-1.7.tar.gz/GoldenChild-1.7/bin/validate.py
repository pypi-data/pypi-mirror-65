#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, re, os, libxml2, argparse, argcomplete, logging

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-s','--schema',  action='store', help='schema name')
parser.add_argument('xml',			action='store', help='xml file')

argcomplete.autocomplete(parser)
args = parser.parse_args()

doc = libxml2.parseFile(args.xml)

if args.schema:
	schema = args.schema
	ctx = doc.xpathNewContext()
	if not doc.getRootElement().ns():
		# if no namespace specified, use the targetNamespace from the schema
		sdoc = libxml2.parseFile(schema)
		tns = sdoc.getRootElement().prop('targetNamespace')
		doc.getRootElement().setProp('xmlns',tns)
		xml = str(doc)
		doc = libxml2.parseDoc(xml)
else:
	schemaElement = doc.getRootElement()
	schemaTag = None
	for tag in ['schemaLocation','noNamespaceSchemaLocation']:
		if schemaElement.hasProp(tag):
			schemaTag = schemaElement.prop(tag)
			break
	if not schemaTag:
		sys.stderr.write('no schema found in doc\n')
		sys.exit(1)
	schemaTags = schemaTag.split(' ')
	spath = schemaTags[len(schemaTags)-1]
	dpath = os.path.dirname(args.xml)
	if len(dpath) == 0:
		schema = spath
	else:
		schema = '%s/%s'%(dpath,spath)

if args.verbose:
	sys.stderr.write('schema=%s\n'%schema)
	logging.getLogger().setLevel(logging.DEBUG)

ctxt = libxml2.schemaNewParserCtxt(schema)
schema = ctxt.schemaParse()
del ctxt

validationCtxt = schema.schemaNewValidCtxt()
instance_Err = validationCtxt.schemaValidateDoc(doc)

del validationCtxt
del schema
doc.freeDoc()

if instance_Err != 0:
	sys.stderr.write('%s: FAILED\n'%args.xml)
	sys.exit(1)
else:
	sys.stdout.write('%s: VALID\n'%args.xml)
	sys.exit(0)
