<?php

/**
 * Client.php generator class
 *
 */
class ClientGenerator
{
    const DS = DIRECTORY_SEPARATOR;

    /**
     * @var array
     */
    private $data = [
        "classes" => []
    ];

    /**
     * @var string
     */
    private $templatesDir = "";

    /**
     * @var string
     */
    private $configFile = "";

    /**
     * @param string $templatesDir
     */
    public function setTemplatesDir(string $templatesDir)
    {
        $this->templatesDir = $templatesDir;
    }

    /**
     * @param string $configFile
     */
    public function setConfigFile(string $configFile)
    {
        $this->configFile = $configFile;
    }

    /**
     * Magic get method (this is used by the view scripts)
     *
     * @param string $name
     * @return mixed
     */
    public function __get($name)
    {
        return $this->get($name);
    }

    /**
     * Returns a variable that is set on the view (if it exists)
     *
     * @param string $name
     * @param mixed $default
     * @return mixed|null
     */
    public function get($name, $default = null)
    {
        if (isset($this->data[$name])) {
            return $this->data[$name];
        }
        return $default;
    }

    /**
     * Runs the generation process
     *
     * @return void
     */
    public function run(): void
    {
        $projectDir = dirname(dirname(__DIR__));
        $config = json_decode(file_get_contents(realpath($this->configFile)), true);
        $clientClassName = $config["clientClassName"];
        $path = $this->templatesDir . DIRECTORY_SEPARATOR . "{$clientClassName}.phtml";
        $apiClassDir = implode(DIRECTORY_SEPARATOR, [
            dirname($projectDir) . DIRECTORY_SEPARATOR . $config["composerProjectName"],
            $config["packagePath"],
            $config["srcBasePath"],
            $config["apiPackage"]
        ]);

        // Merge config
        $this->data = array_merge($this->data, $config);

        // Detect the classes
        $classes = [];
        $files = scandir($apiClassDir);
        if (is_array($files)) {
            foreach ($files as $file) {
                $fullPath = realpath($apiClassDir . DIRECTORY_SEPARATOR . $file);
                if (in_array($file, ['.', '..', "AbstractApi.php", "{$clientClassName}.php"]) || is_dir($fullPath)) {
                    continue;
                }
    
                $clsName = rtrim($file, ".php");
                $classes[$clsName] = "\\" . $config["invokerPackage"] . "\\" . $config["apiPackage"] . "\\" . $clsName;
            }
        }

        $this->data["classes"] = $classes;

        // Render the template
        ob_start();
        require realpath($path);
        $contents = str_replace("<//php_template", "<?php", ob_get_clean());

        // Write the generated file
        file_put_contents($apiClassDir . DIRECTORY_SEPARATOR . "{$clientClassName}.php", $contents);
    }
}

$generator = new ClientGenerator();
$generator->setTemplatesDir($argv[1]);
$generator->setConfigFile($argv[2]);
$generator->run();