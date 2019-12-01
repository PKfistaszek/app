<snippet>
  <content><![CDATA[
  # ${1:App}
  Program responsible for downloading and archive data from https://pypi.org/rss/packages.xml with search possibility.
  ]]>
  ## Enviroment variables
  Add to local_env:
  PAGE_NUMBER - pagination number: integer value.
  example:
  `PAGE_NUMBER = 10`
  ADMIN_ENABLED - admin turn on/off:  bool value.
  example:
  'ADMIN_ENABLED = False'
  ## Restore data
  Enter to  app_web_1 docker `docker exec -it app_web_1 bash` and run commad `python manage.py searchi_index --rebuild`
  </content>
  <tabTrigger>readme</tabTrigger>
</snippet>>
